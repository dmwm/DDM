import httplib2
import urllib
import httplib
import json
import logging
from datetime import datetime, date, timedelta
import time 
import sys
from math import sqrt, factorial
from optparse import OptionParser
from collections import defaultdict
from multiprocessing import Pool
import re
import cx_Oracle
import os

__version__ = 0.1
logger = logging.getLogger('data popularity')

timeformat="%Y-%m-%d %H:%M:%S"
connection_string=""


def set_loggerOptions(options):
    FORMAT = '%(asctime)s %(levelname)s %(message)s'
    
    log_level = logging.WARNING
    if options.verbose:
        log_level = logging.INFO
    if options.debug:
        log_level = logging.DEBUG
                
    logging.basicConfig( format=FORMAT , level = log_level )

    options.logger = logger

    
def do_options():
    """
    Read options and set up a logger
    """

    today = date.today()
        
    default_window = 24 #hours
    default_delta = timedelta(days=default_window)
    start = today - default_delta

    #FIXME: remove the unneeded variables
    
    parser = OptionParser(version="%prog " + str(__version__))
    parser.add_option("-v", "--verbose", dest="verbose",
                    action="store_true", default=False, help="Be more verbose")
    parser.add_option("-d", "--debug", dest="debug",
                    action="store_true", default=False, help="print debugging statements")

    parser.add_option("-w", "--window", dest="window", default=default_window, type="int",
                    help="size of the time window to evaluate popularity over, default %s days" % default_window)

    parser.add_option("-e", "--end", dest="end", default = today.strftime(timeformat),
                    help="end date, dates are formatted as Y-m-d, default: %s" % today.strftime(timeformat))

    parser.add_option("-s", "--start", dest="start", default = start.strftime(timeformat),
                    help="start date, dates are formatted as Y-m-d, default: %s" % start.strftime(timeformat))

    parser.add_option("-f", "--fake", dest="fakeUpload",
                    action="store_true", default=False, help="doesn't upload the data into the DB - Just queries the dashboard for test")
    
    parser.add_option("-b", "--bulk", dest="bulkUpload",
                    action="store_true", default=False, help="use the bulk insertion")

    # parse the input
    options, args = parser.parse_args()
    
    set_loggerOptions(options)

    logger.info('\nPrinting command line options')
    logger.info(options)
    return options

def printStats(start,stop,comment):
    delta=stop - start
    logger.info("\n--------------------------------------\n %s: start %s \t stop %s \t delta %s s \t %s mus\n--------------------------------------\n" % (comment,datetime.strftime(start,timeformat),datetime.strftime(stop,timeformat),delta.seconds,delta.microseconds))
    
def get_url(url):
    """
    Download a URL as json and deserialise to a dict
    """
    print url
    logger.debug('Accessing %s' % url)
    http_handler = httplib2.Http("cache")

    response, data = http_handler.request(url, 'GET',headers={'Accept':'application/json'} )
    
    if int(response['status']) < 400:
        #logger.debug(response)
        return json.loads(data)
    else:
        logger.warning("Didn't get an OK response")
        for k,v in response.items():
            logger.error('%s = %s' % (k, v))
        raise Exception("Failed get_url %s" % url)

def request_data(date_tuple):
    dashboard_url = 'http://dashb-cms-datapop.cern.ch/dashboard/request.py/cms-data-pop-api'

    params = {'start': date_tuple[0].strftime(timeformat),
              'end': date_tuple[1].strftime(timeformat)
              }

    start_time=datetime.now()

    get_url_success = False
    max_attemps = 5
    attempt_count = 0
    while get_url_success == False:
        try:
            dashboard_data = get_url('%s?%s' % (dashboard_url, urllib.urlencode(params)))
            get_url_success = True
        except Exception, err:
            attempt_count+=1
            time_sleep = factorial(attempt_count) * 60
            time.sleep(time_sleep)
            logger.error("Failed to get_url. Attempt %s of %s\n%s\going to sleep for %s s, then retry.)"%(attempt_count,max_attemps,err,time_sleep))
            if attempt_count >= max_attemps:
                raise Exception
        
    stop_time=datetime.now()
    printStats(start_time,stop_time,"time needed to get_url")

    
    #This could be a long print
    #print dashboard_data
    return dashboard_data


def request_data_from_file(filename):

    logger.info('opening file %s' % filename )
    f = open(filename)
    data = json.load(f.read())
    f.close()
    return data
                            
def _refresh_SingleMV(table,mode='F'):
    logger.info('_refresh_SingleMV table %s, mode %s' % (table, mode) )
    
    start_time=datetime.now()

    connection = cx_Oracle.Connection(connection_string)
    cursor = cx_Oracle.Cursor(connection)
    
    cursor.callproc('CMS_POPULARITY_SYSTEM.MVREFRESH',[table,mode]);
    stop_time=datetime.now()
    printStats(start_time,stop_time,table)
    
    connection.commit()
    cursor.close()
    connection.close()


def _refresh_with_alter(table,mode='F'):
    logger.info('_refresh_with_alter table %s, mode %s' % (table, mode) )
    
    start_time=datetime.now()

    connection = cx_Oracle.Connection(connection_string)
    cursor = cx_Oracle.Cursor(connection)

    cursor.execute('alter session set "_replace_virtual_columns"=FALSE')
    cursor.callproc('CMS_POPULARITY_SYSTEM.MVREFRESH',[table,mode]);
    stop_time=datetime.now()
    printStats(start_time,stop_time,table)
    
    connection.commit()
    cursor.close()
    connection.close()


def _refresh_SingleMV_Wrapper(args):
    _refresh_SingleMV(*args)

def _refresh_T_CorruptedFiles():
    start_time=datetime.now()

    connection = cx_Oracle.Connection(connection_string)
    cursor = cx_Oracle.Cursor(connection)
    
    cursor.callproc('CMS_POPULARITY_SYSTEM.CORRUPTEDFILEREFRESH');
    stop_time=datetime.now()
    printStats(start_time,stop_time,'CORRUPTEDFILEREFRESH')
    
    connection.commit()
    cursor.close()
    connection.close()


class DB2DB:
    def __init__(self, config):
        """
        Save the necessary configuration variables
        """
        
        self.config = config
        self.logger = config.logger
        self.http_handler = httplib2.Http("cache")

        #FIXME should be made configurable
        self.connection_string = connection_string

        #-- define time interval
        self.start = datetime.strptime(config.start, timeformat)
        self.end   = datetime.strptime(config.end, timeformat)
        self.hwindow = timedelta(hours=config.window)
        
        self.logger.info( "\n-------------\nstart time is %s " % self.start)
        self.logger.info( "end time is %s " % self.end)
        self.logger.info( "split window is %s (hours) \n-------------\n" % self.hwindow)
        
             
        #-- define data members
        self._getDBConnection()

        self.old_jobid=0
        self.CountJobs=0
        self.CountFiles=0
        self.CountJobsInPop=0
        self.CountFilesInPop=0
        self.CountSingleInsertFailures=0
        self.CountBulkInsertFailures=0

        self.firstPrepare = True
        
        self.old_filename=""
        self.now = datetime.strftime(datetime.utcnow(), timeformat)

        self.PopDBAttribute = {}
        self.PopDBAttributeList = []
        self.PopDBAttributeJobList = []
        self.DashData = defaultdict(list)
        self.attrString =""
        self.dataset_data = defaultdict(dict)


    def __call__(self):
        """
        
        """
        self._populatePopDB()

    def _commit(self):
        if(self.config.fakeUpload == False):
            start_time=datetime.now()
            self.connection.commit()
            stop_time=datetime.now()
            printStats(start_time,stop_time,"time needed to commit connection")
                
    def _populatePopDB(self):
        """
        fill the Data Popularity DB
        """

        start_time=datetime.now()
        self._SequentialUpload()
        stop_time=datetime.now()
        printStats(start_time,stop_time,"time needed to do the sequential upload")
        
        self._commit()
            
        #self.logger.info("\n .... refreshing MV")
        #start_time=datetime.now()
        #self._refresh_MV()
        #stop_time=datetime.now()
        #printStats(start_time,stop_time,"time needed to refresh the PopDb MV")
        #
        #start_time=datetime.now()
        #self.cursor.close()
        #self.connection.close()
        #stop_time=datetime.now()
        #printStats(start_time,stop_time,"time needed to close connection")


    def _getDBConnection(self):

        try:
            self.cursor.close()
            self.connection.close()
        except Exception as inst:
            pass
            #print inst           # __str__ allows args to printed directly

        
        self.connection = cx_Oracle.Connection(self.connection_string)
        self.cursor = cx_Oracle.Cursor(self.connection)


    def _refresh_MV(self):

        mvPool = Pool(3)
        table_input=['MV_DS_Files', 'MV_block_stat0', 'MV_USER_USERID']
        map_input = [ (x,'F') for x in table_input ]        
        mvPool.map(_refresh_SingleMV_Wrapper, map_input)
        mvPool.close()
        
        _refresh_with_alter('MV_DS_STAT0','F')

        mvPool = Pool(10)
        table_input=['MV_DS_STAT0_AGGR1','MV_DS_STAT0_AGGR2','MV_DS_STAT0_AGGR1_SUMM','MV_DS_STAT0_AGGR2_SUMM','MV_DS_STAT0_AGGR3','MV_DS_STAT0_AGGR4','MV_DS_STAT0_AGGR4_SUMM','MV_DS_CountFiles','MV_block_stat0_aggr_5_weeks','MV_DS_stat0_remote']                
        map_input = [ (x,'C') for x in table_input ]        
        mvPool.map(_refresh_SingleMV_Wrapper, map_input)
        mvPool.close()

        mvPool = Pool(6)
        table_input=['MV_DSName','MV_DS','MV_DataTier','MV_Site','MV_block_stat0_last_access','MV_block_stat0_aggr_180_days']
        map_input = [ (x,'C') for x in table_input ]        
        mvPool.map(_refresh_SingleMV_Wrapper, map_input)
        mvPool.close()

        _refresh_T_CorruptedFiles()

        _refresh_SingleMV('MV_CorruptedFiles','C');
        

        
    def _setPopDBAttributes(self,data):
        #print data
        
        PopDBAttribute = {}
        PopDBAttribute["INSERTTIME"]                         = self._set_INSERTTIME		         (data)	   
        PopDBAttribute["FILENAME"]                           = self._set_FILENAME			 (data)	   
        PopDBAttribute["FILESIZE"]                           = self._set_FILESIZE			 (data)	   
        PopDBAttribute["ISPARENT"]                           = self._set_ISPARENT			 (data)	   
        PopDBAttribute["ISREMOTE"]                           = self._set_ISREMOTE			 (data)
        PopDBAttribute["PROTOCOL"]                           = self._set_PROTOCOL			 (data)	   
        PopDBAttribute["LUMIRANGE"]                          = self._set_LUMIRANGE			 (data)	   
        PopDBAttribute["FILEEXECEXITCODE"]                   = self._set_FILEEXECEXITCODE		 (data)	   
        PopDBAttribute["FILESTARTEDRUNNINGTIMESTAMP"]        = self._set_FILESTARTEDRUNNINGTIMESTAMP     (data)	   
        PopDBAttribute["FILEFINISHEDTIMESTAMP"]              = self._set_FILEFINISHEDTIMESTAMP	         (data)	   
        PopDBAttribute["FILERUNNINGTIME"]                    = self._set_FILERUNNINGTIME		 (data)   
        PopDBAttribute["BLOCKID"]                            = self._set_BLOCKID			 (data)   
        PopDBAttribute["BLOCKNAME"]                          = self._set_BLOCKNAME			 (data)	   
        PopDBAttribute["INPUTCOLLECTION"]                    = self._set_INPUTCOLLECTION		 (data)   
        PopDBAttribute["APPLICATION"]                        = self._set_APPLICATION		         (data)	   
        PopDBAttribute["TASKTYPE"]                           = self._set_TASKTYPE			 (data)	   
        PopDBAttribute["SUBMISSIONTOOL"]                     = self._set_SUBMISSIONTOOL 		 (data)   
        PopDBAttribute["INPUTSE"]                            = self._set_INPUTSE			 (data)   
        PopDBAttribute["TARGETCE"]                           = self._set_TARGETCE			 (data)	   
        PopDBAttribute["SITENAME"]                           = self._set_SITENAME			 (data)	   
        PopDBAttribute["SCHEDULERNAME"]                      = self._set_SCHEDULERNAME		  	 (data)	   
        PopDBAttribute["JOBID"]                              = self._set_JOBID			 	 (data)	   
        PopDBAttribute["JOBMONITORID"]                       = self._set_JOBMONITORID		 	 (data)	   
        PopDBAttribute["TASKMONITORID"]                      = self._set_TASKMONITORID		 	 (data)	   
        PopDBAttribute["TASKJOBID"]                          = self._set_TASKJOBID			 (data)	   
        PopDBAttribute["TASKID"]                             = self._set_TASKID 			 (data)   
        PopDBAttribute["JOBEXECEXITCODE"]                    = self._set_JOBEXECEXITCODE		 (data)   
        PopDBAttribute["JOBEXECEXITTIMESTAMP"]               = self._set_JOBEXECEXITTIMESTAMP	         (data)	   
        PopDBAttribute["STARTEDRUNNINGTIMESTAMP"]            = self._set_STARTEDRUNNINGTIMESTAMP	 (data)   
        PopDBAttribute["FINISHEDTIMESTAMP"]                  = self._set_FINISHEDTIMESTAMP		 (data)	   
        PopDBAttribute["WALLCLOCKCPUTIME"]                   = self._set_WALLCLOCKCPUTIME		 (data)	   
        PopDBAttribute["CPUTIME"]                            = self._set_CPUTIME			 (data)   
        PopDBAttribute["USERID"]                             = self._set_USERID 			 (data)   
        PopDBAttribute["USERNAME"]                           = self._set_USERNAME			 (data)	   
        PopDBAttribute["FILETYPE"]                           = self._set_FILETYPE			 (data)	   
        PopDBAttribute["FILEEXITFLAG"]                       = self._set_FILEEXITFLAG			 (data)	   

# Giordano 28/11/2011
# adding these additional attributes to take into account the possibility of truncated strings
        PopDBAttribute["STRIPPEDFILES"]                         = self._set_STRIPPEDFILES			 (data)	   
        PopDBAttribute["STRIPPEDPARENTFILES"]                   = self._set_STRIPPEDPARENTFILES		 (data)	   
        PopDBAttribute["STRIPPEDBLOCKS"]                        = self._set_STRIPPEDBLOCKS			 (data)	   
        PopDBAttribute["STRIPPEDLUMIS"]                         = self._set_STRIPPEDLUMIS			 (data)	   


        if self.config.debug :
            print "---------------------------" 
            for field,val in data.items():
                print "%s \t %s " % (field,val)

        self.CountFiles+=1

        if ( self.old_jobid == 0 ):
            self.old_jobid = PopDBAttribute["JOBID"]
            self.CountFilesInJobWithFlagOne=0 #initialize counter
            
        if ( PopDBAttribute["JOBID"] != self.old_jobid ):
            self._SummarizeJobInfo(self.PopDBAttributeJobList,self.CountFilesInJobWithFlagOne)
            self.CountJobs+=1
            
            self._insertDataToPopDB(self.PopDBAttributeJobList)
                
            del self.PopDBAttributeJobList[:]
            self.old_jobid = PopDBAttribute["JOBID"]
            self.CountFilesInJobWithFlagOne=0 #initialize counter

        #Do in both cases PopDBAttribute["JOBID"] == self.old_jobid or != self.old_jobid  
        self.PopDBAttributeJobList.append(PopDBAttribute)
        if(PopDBAttribute["FILEEXITFLAG"]==1):
            self.CountFilesInJobWithFlagOne+=1


    def _set_INSERTTIME			(self,data):
        return '%s' % self.now

    def _set_FILENAME			(self,data):
        return  str(data["FileName"])

    def _set_FILESIZE			(self,data):
        return 0 # FIXME data["FILESIZE"]

    def _set_ISPARENT			(self,data):
        return data["IsParentFile"]

    def _set_ISREMOTE			(self,data):
        if re.search('[u,U]nknown', data["ProtocolUsed"]) :
            return -1
        elif re.search('Local', data["ProtocolUsed"]) :
            return 0
        else:
            return 1

    def _set_PROTOCOL			(self,data):
        return  str(data["ProtocolUsed"])

    def _set_LUMIRANGE			(self,data):
        return  str(data["LumiRanges"])

    def _set_FILEEXECEXITCODE		(self,data):
        return 0 # FIXME data["FILEEXECEXITCODE"]

    def _set_FILESTARTEDRUNNINGTIMESTAMP	(self,data):
        return '2011-01-01 00:00:00'

    def _set_FILEFINISHEDTIMESTAMP		(self,data):
        return '2011-01-01 00:00:00'

    def _set_FILERUNNINGTIME		(self,data):
        return 0 # FIXME data["FILERUNNINGTIME"]

    def _set_BLOCKID			(self,data):
        return data["BlockId"]

    def _set_BLOCKNAME			(self,data):
        return str(data["BlockName"])

    def _set_INPUTCOLLECTION		(self,data):
        return str(data["InputCollection"])

    def _set_APPLICATION			(self,data):
        return str(data["Application"])

    def _set_TASKTYPE			(self,data):
        return str(data["Type"])

    def _set_SUBMISSIONTOOL 		(self,data):
        return str(data["SubmissionTool"])

    def _set_INPUTSE			(self,data):
        return str(data["InputSE"])

    def _set_TARGETCE			(self,data):
        return str(data["TargetCE"])

    def _set_SITENAME			(self,data):
        return str(data["SiteName"])

    def _set_SCHEDULERNAME			(self,data):        
        return str(data["SchedulerName"])

    def _set_JOBID				(self,data):
        return data["JobId"]

    def _set_JOBMONITORID			(self,data):
        return str(data["JobMonitorId"])

    def _set_TASKMONITORID			(self,data):
        return str(data["TaskMonitorId"])

    def _set_TASKJOBID			(self,data):
        return data["TaskJobId"]

    def _set_TASKID 			(self,data):
        return data["TaskId"]

    def _set_JOBEXECEXITCODE		(self,data):
        if(data["JobExecExitCode"] == None):
            return -1
        return data["JobExecExitCode"]

    def _set_JOBEXECEXITTIMESTAMP		(self,data):
        return str(data["JobExecExitTimeStamp"]).replace("T"," ")

    def _set_STARTEDRUNNINGTIMESTAMP	(self,data):
        return  str(data["StartedRunningTimeStamp"]).replace("T"," ")

    def _set_FINISHEDTIMESTAMP		(self,data):
        return str(data["FinishedTimeStamp"]).replace("T"," ")

    def _set_WALLCLOCKCPUTIME		(self,data):
        return data["WrapWC"]
    
    def _set_CPUTIME			(self,data):
        return data["WrapCPU"]

    def _set_USERID			(self,data):
        return data["UserId"]

    def _set_USERNAME			(self,data):
        return str(data["GridName"])

    def _set_FILETYPE			(self,data):
        return str(data["FileType"])

    def _set_FILEEXITFLAG		(self,data):
        return data["SuccessFlag"]                   

# Giordano 28/11/2011
# adding these additional attributes to take into account the possibility of truncated strings
# for the time being, before implementation of this information in the Dashboard API
# the value is the default (0), meaning that there was not truncation
    def _set_STRIPPEDFILES			 (self, data):
        return data["StrippedFiles"]
    def _set_STRIPPEDPARENTFILES		 (self, data):
        return 0
    def _set_STRIPPEDBLOCKS		 (self, data):
        return data["StrippedBlocks"]
    def _set_STRIPPEDLUMIS			 (self, data):
        return 0
    

    def _SummarizeJobInfo(self,sameJobFileList,filesCounter):

        # for entry in sameJobFileList:
        #     if ( entry["FILEEXITFLAG"] != 1):
        #         entry["CPUTIME"]=0
        #     else:
        #         entry["CPUTIME"]=entry["CPUTIME"]/filesCounter

        for i in range(len(sameJobFileList)):
            if ( sameJobFileList[i]["FILEEXITFLAG"] != 1):
                sameJobFileList[i]["CPUTIME"]=0
            else:
                sameJobFileList[i]["CPUTIME"]=sameJobFileList[i]["CPUTIME"]/filesCounter
     
    def _get_TimeDelta(self, secs):
        seconds_in_day=24*3600  #NB: this must be integer to work 
        return  timedelta(days=(secs/seconds_in_day) , seconds=(secs%seconds_in_day))
        

    def _get_ranges(self,map_input):
        delta = self.end - self.start
        self.logger.info( " delta end - start %s (days) %s (seconds) " % (delta.days, delta.seconds))
        self.logger.info( " split window %s (days) %s (seconds) " % (self.hwindow.days,self.hwindow.seconds))
        tot_seconds=delta.days*24*3600 +delta.seconds
        wind_seconds=self.hwindow.days*24*3600 + self.hwindow.seconds
        size = tot_seconds /  wind_seconds
      
        self.logger.info("split size %s " % size)
        self.logger.debug('Starting %s processes' % size)

        for i in range(size):
            thestart = self.start + self._get_TimeDelta( i * wind_seconds )
            thestop  = self.start + self._get_TimeDelta( (i+1) * wind_seconds )  
            map_input.append((thestart, thestop))
        if tot_seconds%wind_seconds :
            if size:
                i=i+1
            else:
                i=0
            thestart = self.start + self._get_TimeDelta( i * wind_seconds )
            thestop  = self.end
            map_input.append((thestart, thestop))

        self.logger.info('\nList of api query time ranges')
        self.logger.info(map_input)


    def _SequentialUpload(self):
        """
        access the Dashboard and retrieve the needed data, using Eddy API
        """

        map_input = []
        self._get_ranges(map_input)

        for args in map_input:
            self.logger.info(args)
            DashData = request_data(args)
            #DashData = request_data_from_file("A.txt")

            self._HandleData(DashData)
            self.logger.info("\n--------------------------------------\nNumber of failed insert : bulk %s \t,\t single %s\n--------------------------------------\n" % (self.CountBulkInsertFailures,self.CountSingleInsertFailures))


        self.logger.info("\n--------------------------------------\nsize of the buffer retrieved from Dashboard %d \nNumber of jobs %s \n--------------------------------------\n" % (self.CountFiles,self.CountJobs))
        self.logger.info("\n--------------------------------------\nsize of the buffer uploaded into PopDB %d \nNumber of jobs %s      \n--------------------------------------\n" % (self.CountFilesInPop,self.CountJobsInPop))

                
        
    def _HandleData(self,data):
        """
        organize data following the Data Popularity DB Schema
        """
        for entry in data['jobs']:
            #print entry
            self._setPopDBAttributes(entry)        
        

    def _insertDataToPopDB(self,dataList):
        """
        insert data into PopDB
        """

        self.cursor.execute("alter session set NLS_DATE_FORMAT='YYYY-MM-DD HH24:MI:SS'")

        self.countEntries=len(dataList);
        self.countInsertedEntries=0;

        if(self.config.bulkUpload == True):
            self._bulkInsert(dataList)
        else:
            self._singleInsertSequence(dataList)


    def _singleInsertSequence(self,dataList):

        if self.firstPrepare:
            self._prepareStatement(dataList)

        for row in dataList:

            try:
                if(self.config.fakeUpload == False):
                    self.cursor.execute(self.statement,row)
                    self.countInsertedEntries+=1
            except Exception as inst:
                self.CountSingleInsertFailures+=1
                self.logger.error("\n---------------------------\nthere is an error in inserting the statement :\n\t%s\n---------------------------\n" % self.statement)
                self.logger.error(inst)           # __str__ allows args to printed directly
                #print ' '
                #print row
                #for key,val in row.items():
                #    print '%s \t %s' % (key,val)
                

#        if(self.config.fakeUpload == False):
#            self.connection.commit()


    def _prepareStatement(self,dataList):
        row = dataList[0]
        attrString=""
        attrVal=""
        first=True
        for key,val in row.items():
            if (first):
                attrString = ":%s" % key
                first=False
                attrVal = "%s" % val
            else:
                attrString = "%s, :%s" % (attrString,key)
                attrVal = "%s, %s " % (attrVal,val)
                
        valuesAttr = attrString

        self.statement = "insert into  CMS_POPULARITY_SYSTEM.RAW_FILE( %s ) values( %s )" % (valuesAttr.replace(":",""),attrString)
        #self.cursor.prepare(self.statement)
        self.firstPrepare= False
        

    def _bulkInsert(self,dataList):
        
        #self.logger.info(statement)
        try:
            #self.logger.info("bulk insertion")

            if self.firstPrepare:
                self._prepareStatement(dataList)
                
            if(self.config.fakeUpload == False):
                self.cursor.executemany(self.statement,dataList)

            self.countInsertedEntries=len(dataList);

            self.CountJobsInPop+=1
            self.CountFilesInPop+=self.countInsertedEntries


        except Exception as inst:

            if self.CountBulkInsertFailures%10000==0 :
                self.logger.error("\n---------------------------\nthere is an error in inserting the statement :\n\t%s\n---------------------------\n %s \n %s" % (self.statement,dataList, inst))
                    
            self.CountBulkInsertFailures+=1

            #for row in self.PopDBAttributeList:
                #print "\n++++++++++++++++++++++++\n"
                #print row
                #for key,val in row.items():
                #    print '%s \t %s' % (key,val)

        
#------------------------------------------------------

if __name__ == '__main__':
    f = open('./etc/auth.txt')
    authParams = json.loads(f.read())
    connection_string  = authParams['DB_CONN_STRING']
    config = do_options()
    dbTOdb = DB2DB(config)
    dbTOdb()

