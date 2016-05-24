from __future__ import print_function
import httplib2
import urllib
import httplib
import json
import logging
from datetime import datetime, date, timedelta
import time 
import sys
from math import sqrt
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

#----------------------------------------------------------------------------------------------------------------------------
def set_loggerOptions(options):
    log_level = logging.WARNING
    if options.verbose:
        log_level = logging.INFO
    if options.debug:
        log_level = logging.DEBUG
    logging.basicConfig(level=log_level)
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

    parser.add_option("-c", "--cron", dest="cronMode",
                    action="store_true", default=False, help="adopt configuration for cron. The start date is retrieved from the PopDB last entry, and the end date is \'yesterday\'")

    parser.add_option("-l", "--light", dest="lightMode",
                      action="store_true", default=False, help="does upload of the rows for each jobs, not storing the full bulk of data. reduces the memory overload")


    # parse the input
    options, args = parser.parse_args()
    
    set_loggerOptions(options)

    logger.info('\nPrinting command line options')
    logger.info(options)
    return options

def printStats(start, stop, comment):
    delta=stop - start
    logger.info("\n--------------------------------------\n %s: start %s \t stop %s \t delta %s s \t %s mus\n--------------------------------------\n" % (comment, datetime.strftime(start, timeformat), datetime.strftime(stop, timeformat), delta.seconds, delta.microseconds))
    
def get_url(url):
    """
    Download a URL as json and deserialise to a dict
    """
    print(url)
    logger.debug('Accessing %s' % url)
    http_handler = httplib2.Http("cache")

    response, data = http_handler.request(url, 'GET', headers={'Accept':'application/json'} )
    
    if int(response['status']) < 400:
        #logger.debug(response)
        return json.loads(data)
    else:
        logger.warning("Didn't get an OK response")
        #for k,v in response.items():
        #    logger.info('%s = %s' % (k, v))

def request_data(date_tuple):
    dashboard_url = 'http://dashb-cms-datapop.cern.ch/dashboard/request.py/cms-data-pop-api'

    params = {'start': date_tuple[0].strftime(timeformat),
              'end': date_tuple[1].strftime(timeformat)
              }

    start_time=datetime.now()
    dashboard_data = get_url('%s?%s' % (dashboard_url, urllib.urlencode(params)))
    stop_time=datetime.now()
    printStats(start_time, stop_time, "time needed to get_url")

    
    #This could be a long print
    #print dashboard_data
    return dashboard_data


def request_data_from_file(date_tuple):

    print("open file ")
    print(str(date_tuple))
    json_data=open(str(date_tuple))
    data = json.load(json_data)
    #pprint(data)
    json_data.close()
    return data
                            
def _refresh_SingleMV(table,mode='F'):
    logger.info('_refresh_SingleMV table %s, mode %s' % (table, mode) )
    
    start_time=datetime.now()

    connection = cx_Oracle.Connection(connection_string)
    cursor = cx_Oracle.Cursor(connection)
    
    cursor.callproc('CMS_POPULARITY_SYSTEM.MVREFRESH', [table, mode]);
    stop_time=datetime.now()
    printStats(start_time, stop_time, table)
    
    connection.commit()
    cursor.close()
    connection.close()


def _refresh_with_alter(table,mode='F'):
    logger.info('_refresh_with_alter table %s, mode %s' % (table, mode) )
    
    start_time=datetime.now()

    connection = cx_Oracle.Connection(connection_string)
    cursor = cx_Oracle.Cursor(connection)

    cursor.execute('alter session set "_replace_virtual_columns"=FALSE')
    cursor.callproc('CMS_POPULARITY_SYSTEM.MVREFRESH', [table, mode]);
    stop_time=datetime.now()
    printStats(start_time, stop_time, table)
    
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
    printStats(start_time, stop_time, 'CORRUPTEDFILEREFRESH')
    
    connection.commit()
    cursor.close()
    connection.close()

#----------------------------------------------------------------------------------------------------------------------------

class DB2DB:
    def __init__(self, config):
        """
        Save the necessary configuration variables
        """
        
        self.config = config
        self.logger = config.logger
        self.http_handler = httplib2.Http(".cache")

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
            printStats(start_time, stop_time, "time needed to commit connection")
                
    def _populatePopDB(self):
            
        self.logger.info("\n .... refreshing MV")
        start_time=datetime.now()
        self._refresh_MV()
        stop_time=datetime.now()
        printStats(start_time, stop_time, "time needed to refresh the PopDb MV")

        start_time=datetime.now()
        self.cursor.close()
        self.connection.close()
        stop_time=datetime.now()
        printStats(start_time, stop_time, "time needed to close connection")


    def _getDBConnection(self):

        try:
            self.cursor.close()
            self.connection.close()
        except Exception as inst:
            a=1
            #print inst           # __str__ allows args to printed directly

        
        self.connection = cx_Oracle.Connection(self.connection_string)
        self.cursor = cx_Oracle.Cursor(self.connection)


    def _set_TimeWindow(self):
        
        query = "select to_char(max(finishedtimestamp),'yyyy-mm-dd hh24:mi:ss') from  CMS_POPULARITY_SYSTEM.raw_file"
        self.cursor.execute(query)

        row = self.cursor.fetchone()[0]

        starttime = datetime.strptime(row, timeformat)+timedelta(seconds=1)    
        endtime = datetime.strptime((date.today()).strftime(timeformat), timeformat)

        self.logger.info("\n---------------\nCron Mode. Redefine Query Time Window")
        self.logger.info("New starttime %s " % starttime)
        self.logger.info("New endtime %s " % endtime)
        self.start = starttime
        self.end = endtime
            


    def _refresh_MV(self):

        #mvPool = Pool(7)
        #map_input=['MV_USER','MV_JOB','MV_TASK','MV_block_local_noparent','MV_POP_DS_SITE','MV_BLOCK_MAP','MV_POP_BLOCK_SITE']        


        #mvPool = Pool(6)
        #map_input=['MV_DS_STAT0','MV_DS_Files', 'MV_block_stat0', 'MV_USER_USERID', 'MV_CorruptedFiles', 'MV_CorruptedFiles_A']        


        mvPool = Pool(3)
        table_input=['MV_DS_Files', 'MV_block_stat0', 'MV_USER_USERID'] #,'MV_CorruptedFiles']        
        map_input = [ (x, 'F') for x in table_input ]        
        mvPool.map(_refresh_SingleMV_Wrapper, map_input)
        mvPool.close()
        
        _refresh_with_alter('MV_DS_STAT0', 'F')

        mvPool = Pool(16)
        table_input=['MV_DS_STAT0_AGGR1', 'MV_DS_STAT0_AGGR2', 'MV_DS_STAT0_AGGR1_SUMM', 'MV_DS_STAT0_AGGR2_SUMM', 'MV_DS_STAT0_AGGR3', 'MV_DS_STAT0_AGGR4', 'MV_DS_STAT0_AGGR4_SUMM',
                     'MV_DS_STAT1_AGGR1', 'MV_DS_STAT1_AGGR2', 'MV_DS_STAT1_AGGR1_SUMM', 'MV_DS_STAT1_AGGR2_SUMM', 'MV_DS_STAT1_AGGR4', 'MV_DS_STAT1_AGGR4_SUMM',
                     'MV_DS_CountFiles', 'MV_block_stat0_aggr_5_weeks', 'MV_DS_stat0_remote']                
        map_input = [ (x, 'C') for x in table_input ]        
        mvPool.map(_refresh_SingleMV_Wrapper, map_input)
        mvPool.close()

        mvPool = Pool(7)
        table_input=['MV_DSName', 'MV_DS', 'MV_DataTier', 'MV_Site', 'MV_block_stat0_last_access', 'MV_block_stat0_aggr_180_days', 'MV_block_stat0_aggr_12_months']
        map_input = [ (x, 'C') for x in table_input ]        
        mvPool.map(_refresh_SingleMV_Wrapper, map_input)
        mvPool.close()

        _refresh_T_CorruptedFiles()

        _refresh_SingleMV('MV_CorruptedFiles', 'C');
        

        
        
    def _connectToPopDB(self):
        """
        connect to the PopDB
        """
        
        self.logger.info('the tnsentry is %s' % (self.connection.tnsentry))
        
        
#------------------------------------------------------

if __name__ == '__main__':
    f = open('./etc/auth.txt')
    authParams = json.loads(f.read())
    connection_string  = authParams['DB_CONN_STRING']
    config = do_options()
    dbTOdb = DB2DB(config)
    dbTOdb()

