#!/usr/bin/python

import json
import time
import cx_Oracle
from datetime import datetime, timedelta
import logging
import os
import signal
import subprocess

from phedexInterface.phedexRequest import PHEDEXInterface

TIMEFORMAT = "%Y-%m-%d %H:%M:%S"

MAX_ALLOWED_PROCESS_MEMORY = 2000000

class fileToDataSetAssociator:

    def __init__(self, config):

        self.config = config

        self.cursorQ = None
        self.cursor = None
        self.connection = None

        self.logger = self.set_loggerOptions()

        config = open('./etc/auth.txt') #FIXME, introduce config parser
        auth_params = json.loads(config.read())
        self.connection_string = auth_params['DB_CONN_STRING']
        self.connectToDB()

        self.eosPrefix = '/eos/cms'
        self.dataForUser = []
        self.dataForLFC  = []
        self.filesInsertedInLFC = []
        self.filesInsertedInUser = []

        self.countPhEDExQueries = 0
        self.countPhEDExDSQueries = 0
        self.countPhEDExFileQueries = 0


        self.last_updated_insertTime = -1 
        self.last_insertTime = -1
        self.resultUploadUser = True
        self.resultUploadLFC = True


    def set_loggerOptions(self):
        
        log_level = logging.WARNING
        if self.config.verbose:
            log_level = logging.INFO
        if self.config.debug:
            log_level = logging.DEBUG


        FORMAT = '%(asctime)s %(levelname)s %(message)s'
        logging.basicConfig( format=FORMAT , level = log_level )
        logger = logging.getLogger('fileToDataSetAssociator')
        logger.setLevel(level = log_level)
        logger.info(self.config)

        return logger
        
    def printStats(self, start, stop, comment):
        delta = stop - start
        self.logger.info("\n--------------------------------------\n %s: start %s \t stop %s \t delta %s s \t %s mus\n--------------------------------------\n" % (comment, datetime.strftime(start, TIMEFORMAT), datetime.strftime(stop, TIMEFORMAT), delta.seconds, delta.microseconds))


#-----------------------------------------------------------------
# DB utilities
#-----------------------------------------------------------------

    def connectToDB(self):
        self.logger.debug( "\n----------\nConnectToDB\n----------\n")
        self.connection = cx_Oracle.Connection(self.connection_string)
        self.resetCursor()
        
    def resetCursor(self):

        try:
            self.cursorQ.close()
            self.cursor.close()
        except Exception:   
            self.logger.error( "the cursor doesn't exist: going to create it" )

        self.cursorQ = cx_Oracle.Cursor(self.connection)
        self.cursor = cx_Oracle.Cursor(self.connection)

        self.cursorQ.execute("alter session set NLS_DATE_FORMAT='YYYY-MM-DD HH24:MI:SS'")
        self.cursor.execute("alter session set NLS_DATE_FORMAT='YYYY-MM-DD HH24:MI:SS'")

        
    def closeConn(self):
        self.cursor.close()
        self.connection.close()


    def prepareStatement(self, tableName, dataList):
    
        row = dataList[0]
        attrString = ""
        for key in row.keys():
            attrString = "%s, :%s" % (attrString, key)
            
        valuesAttr = attrString.lstrip(",")
            
        statement = "insert into %s( %s ) values( %s )" % (tableName, valuesAttr.replace(":", ""), valuesAttr)

        self.logger.debug( "\n----------\nprepareStatement\n----------\n%s" % statement)
                
        return statement

        
#-----------------------------------------------------------------
# DB upload
#-----------------------------------------------------------------
    
    def concreteUploadToDB(self, statement, data):
        self.logger.debug( "\n----------\nUploadToDB\n----------\n")


        if(self.config.fakeUpload):
            self.logger.info("[concreteUploadToDB] fake Upload: not committing")
        else:
            self.cursor.executemany(statement, data)
            self.connection.commit()
        self.logger.info( "uploaded to DB data %s" % len(data))
        
    def uploadDataToDB(self):    

        if len(self.dataForLFC) > 0:
            self.resultUploadLFC = self.uploadData('T_XRD_LFC', self.dataForLFC)
            
        if len(self.dataForUser) > 0:
            self.resultUploadUser = self.uploadData('T_XRD_USERFILE', self.dataForUser)

    def uploadData(self, tableName, data):

        try:
            statement = self.prepareStatement(tableName, data)

            #patched to include fullname in T_XRD_LFC
            if tableName == 'T_XRD_LFC':
                statement = "insert into T_XRD_LFC(  lfn, dsname, blockname, fullname ) values(  :lfn, :dsname, :blockname, '%s' || :lfn )" % self.eosPrefix
            
            self.concreteUploadToDB(statement, data)
            self.logger.info( 'Uploaded data into DB table %s \tsize %s' % (tableName , len(data) ) )
            del data[:]
            return True
        except Exception, err :
            self.logger.error( 'failing upload data to table %s \nstatement %s\n%s\n%s' % (tableName, statement, Exception, err))

            try:
                newstatement = ''
                if tableName == 'T_XRD_LFC':
                    newstatement = self.newStatementLFC(statement)
                elif tableName == 'T_XRD_USERFILE':
                    newstatement = self.newStatementUSERFILE(statement)
                else:
                    raise ValueError

                self.mergeUploadToDB(newstatement, data)
                return True
            except Exception, err :
                self.logger.error( 'failing also mergeUpload data to table %s \nstatement %s\n%s\n%s\nData %s' % (tableName, newstatement, Exception, err, data))
                raise err
            

    def mergeUploadToDB(self, newstatement, data):
        self.logger.info( "mergeUploadToDB")            
        self.cursor.executemany(newstatement, data)
        self.connection.commit()
        del data[:]
        self.logger.info( 'mergeUploaded data into DB table' )

    def newStatementLFC(self, statement):
        #patched to include fullname in T_XRD_LFC
        newstatement = '''
        merge into T_XRD_LFC t
        using dual
        ON ( t.fullname = \'%s\' || :lfn  )              
        WHEN not MATCHED THEN
        INSERT /*+ APPEND */ %s
        '''% (self.eosPrefix, statement.replace("insert into T_XRD_LFC", ""))

        return newstatement

    def newStatementUSERFILE(self, statement):
        newstatement = '''
        merge into T_XRD_USERFILE t
        using dual
        ON ( t.username = :username )
        WHEN not MATCHED THEN
        INSERT /*+ APPEND */ %s
        '''% statement.replace("insert into T_XRD_USERFILE", "")

        return newstatement

    def updateLastUID(self):
        if self.config.fakeUpload:
            return
        now = time.strftime(TIMEFORMAT, time.gmtime())
        #statement = 'update T_XRD_LAST_UID set unique_id= %s ' % self.last_insertTime
        statement = '''
        insert into T_XRD_LAST_UID (last_insertTime , updatetime)
        values ( to_date(\'%s\', \'YYYY-MM-DD HH24:MI:SS\')  , to_date(\'%s\',\'YYYY-MM-DD HH24:MI:SS\') )
        ''' % (self.last_insertTime, now)
        self.cursor.execute(statement)
        self.connection.commit()
        self.logger.info('updated LastUID with statement \t %s' % statement)


        
        
#-----------------------------------------------------------------
# DB query
#-----------------------------------------------------------------

    def fillTmpTableNewFiles(self):

        # --clean the tmp table of selected files
        query = 'select count(*) from T_xrd_select_files_tmp'
        self.cursorQ.execute(query)
        row = self.cursorQ.fetchone()[0]

        if row > 0:
            #self.logger.info('fillTmpTableNewFiles need to truncate table T_xrd_select_files_tmp' )
            query = 'truncate table T_xrd_select_files_tmp'
            self.cursorQ.execute(query)
            self.connection.commit()
            #self.logger.info('fillTmpTableNewFiles truncated table T_xrd_select_files_tmp' )

        # --fill the tmp table

        query = '''
        insert into T_xrd_select_files_tmp (file_lfn)
        SELECT distinct file_lfn FROM T_XRD_RAW_FILE
        where insertTimeStamp >= \'%s\'
        and insertTimeStamp < \'%s\'
        and
        file_lfn not like \'%s\'
        ''' % (datetime.strftime(self.last_updated_insertTime, TIMEFORMAT),
               datetime.strftime(self.last_insertTime, TIMEFORMAT)
               , '%replicate%')
        #self.logger.info('fillTmpTableNewFiles statement to insert into tmp table %s ' % query)

        self.cursorQ.execute(query)
        self.connection.commit()
        #self.logger.info('fillTmpTableNewFiles inserted data in tmp table')
           

    def fillTmpTableLFNFiles(self):

        # --clean the tmp table of already known lfn
        query = 'select count(*) from T_xrd_lfn_files_tmp'
        self.cursorQ.execute(query)
        row = self.cursorQ.fetchone()[0]

        if row > 0:
            #self.logger.info('fillTmpTableLFNFiles need to truncate table T_xrd_lfn_files_tmp' )
            query = 'truncate table T_xrd_lfn_files_tmp'
            self.cursorQ.execute(query)
            self.connection.commit()
            #self.logger.info('fillTmpTableLFNFiles truncated table T_xrd_lfn_files_tmp' )

        # --fill the tmp table

        query = '''
        insert into T_xrd_lfn_files_tmp (lfn)
        (
        select fullname  as lfn from  T_XRD_LFC
        union all
        select lfn from T_XRD_USERFILE
        )
        ''' 
        #self.logger.info('fillTmpTableLFNFiles statement to insert into tmp table %s ' % query)

        self.cursorQ.execute(query)
        self.connection.commit()
        #self.logger.info('fillTmpTableLFNFiles inserted data in tmp table')
           

    def getNewDataFromDB(self):

        self.fillTmpTableNewFiles()

        query = '''
        select file_lfn from T_xrd_select_files_tmp
        where
        file_lfn not in ( select fullname from  T_xrd_lfc )
        and
        file_lfn not in ( select lfn from T_XRD_USERFILE  )
        '''

        self.cursorQ.execute(query)
        return self.cursorQ

    def getLastUpdatedInsertTime(self):
        
        query = 'select max(last_insertTime) from T_XRD_LAST_UID'
        try:
            self.cursorQ.execute(query)
            row = self.cursorQ.fetchone()[0]
            self.logger.info('Last Updated insertTime %s', row)
            return row
        except Exception, err:
            self.logger.error('error in performing the query %s' % query )
            raise err
        
    
    def getLastInsertTime(self):
        query = 'select max(insertTimestamp) from T_XRD_RAW_FILE'
        self.cursorQ.execute(query)
        row = self.cursorQ.fetchone()[0]
        
        self.logger.info('Last insertTime %s', row)
        
        delta = (row - self.last_updated_insertTime)
        days = delta.days
        seconds = delta.seconds
        N_hours = 6
        
        if  days > 0 or ( days == 0 and delta.seconds > N_hours * 3600 ) : # working on slots of N hours
            self.logger.info('Redefining Interval because longer than max slot: days %s hours %s ' % (days, seconds/3600) )

            
            row = self.last_updated_insertTime + timedelta(hours=N_hours)

            
            self.logger.info('FORCING Last UID %s', row)

        return row


#-----------------------------------------------------------------
# PhEDEx interface
#-----------------------------------------------------------------

    def queryPhedexForFile(self, filename):
        query = 'file=%s' % filename
        self.countPhEDExFileQueries += 1 
        return self.queryPhedex(query)

    def queryPhedexForDS(self, dsname):
        query = 'dataset=%s' % dsname
        self.countPhEDExDSQueries += 1 
        return self.queryPhedex(query)

    def queryPhedex(self, query):

        i = 0
        succeed = False
        while i < 5 and not succeed :
            i += 1
            ( succeed , data ) = self.concreteQueryPhedex(query)
            
        return (succeed , data )

    def concreteQueryPhedex(self, query):
        try:
            myPhedex = PHEDEXInterface(debug=False)
            data = myPhedex.get_phedex_data(self.config.host, query)
            dicData = [ {'dsname':x[0] , 'blockname':x[1], 'lfn':x[2]} for x in data ]
            #print 'final result\n' , dicData

            self.countPhEDExQueries += 1 
            return ( True , dicData )
        
        except Exception, err:
            self.logger.error("Error from PhEDEx interface \n%s" % err)
            return ( False , [] )


#-----------------------------------------------------------------

    def updateAssociations(self):

        self.getNewDataFromDB()

        data = self.cursorQ.fetchmany()
        while len(data) > 0 :
            self.logger.info('got list of files of size %s ' % len(data))
            self.loopOnData(data)
            self.logger.info('fetching other data')
            data = self.cursorQ.fetchmany()

        self.logger.info('Number of Queries to PhEDEx (concrete, file, ds) : (%s, %s, %s)' % (self.countPhEDExQueries, self.countPhEDExFileQueries, self.countPhEDExDSQueries))
        
    def loopOnData(self, data):


        for item  in data:
            eosfile = item[0]
            lfnfile = eosfile.replace(self.eosPrefix, '', 1)
            
            self.logger.debug( "\n-------\n file %s" % eosfile )

            if eosfile.find('/store/backfill/') != -1:
                continue
            if eosfile.find('/store/t0temp/') != -1:
                continue
            if eosfile.find('/store/unmerged/') != -1:
                continue
            if eosfile.find('/store/t0streamer/') != -1:
                continue
            if eosfile.find('/eos/pps/') != -1:
                continue
            if eosfile.find('/eos/ppsscratch/') != -1:
                continue
            if eosfile.find('/eos/cms/opstest/') != -1:
                continue
            
            # do not spend time to search for files already discovered
            # using another file of the same block
            if lfnfile in self.filesInsertedInLFC :
                self.logger.debug('file already discovered %s' % lfnfile)
                continue 
                        
            (result , fileInfo) = self.queryPhedexForFile(lfnfile)

            if result and len(fileInfo) :

                # reconver the information of the full DS
                if not self.getFullDSInfo(fileInfo) :
                    self.dataForLFC.extend(fileInfo)
                    self.filesInsertedInLFC.append(lfnfile)

            else:
                self.updateUserFileTable(eosfile)


        self.uploadDataToDB()

    def getFullDSInfo(self, fileInfo):

        #print 'fileInfo ' , fileInfo
        dsname = fileInfo[0]['dsname']
        (result , filesInfo) = self.queryPhedexForDS(dsname) 

        files = [ x['lfn'] for x in filesInfo ]
        
        if result and len(files) :
            self.dataForLFC.extend(filesInfo)
            self.filesInsertedInLFC.extend(files)
            return True
        else:
            self.logger.error("THIS SHOULD NEVER HAPPEN \n: found a file in PhEDEx, but not the entire DS \n file %s \n DS %s" % (fileInfo[0]['file'], dsname) ) #fixme I still do not know the format
            return False
#-----------------------------------------------------------------

    def updateUserFileTable(self, filename):
        self.logger.debug('userfiles %s' % self.filesInsertedInUser)

        if filename in self.filesInsertedInUser :
            return
        
        userName = 'unknown'
        
        if filename.find('/user/') != -1:
            userName = self.extractUser('user', filename)
        elif filename.find('/group/') != -1:
            userName = self.extractUser('group', filename)
        elif filename.find('/lhe/') != -1:
            userName = 'lhe'
        elif filename.find('/relval/') != -1:
            userName = 'relval'
        elif filename.find('/data/Commissioning') != -1:
            userName = self.extractUser('data', filename)
                        
        self.dataForUser.append({'lfn': filename , 'username' : userName})
        self.filesInsertedInUser.append(filename)
        
        if userName == 'unknown':
            self.logger.warning('unknown user for file %s' % filename)
            
    def extractUser(self, key, filename):
        l = filename.split('/')
        return l[l.index(key)+1]
    
#-----------------------------------------------------------------

    def checkNewUIDs(self):

        self.last_updated_insertTime = self.getLastUpdatedInsertTime()
        self.last_insertTime         = self.getLastInsertTime()

        if self.last_insertTime > self.last_updated_insertTime:
            self.logger.info("There could be new entries to update: %s (last_updated_insertTime) < %s (last_insertTime)  " %  (self.last_updated_insertTime,  self.last_insertTime) ) 
            return True
        elif self.last_insertTime == self.last_updated_insertTime:
            self.logger.info("There are NO entries to update: last_updated_insertTime == last_insertTime == %s" % (self.last_updated_insertTime) )
            return False
        else:
            self.logger.error("THIS SHOULD NEVER HAPPEN : %s (last_updated_insertTime) >  %s (last_insertTime)  " %  (self.last_updated_insertTime, self.last_insertTime) ) 
            #raise ValueError
            return False
        
    def reset(self):
        del self.dataForUser[:]
        del self.dataForLFC[:]
        del self.filesInsertedInLFC[:]
        del self.filesInsertedInUser[:]
        
        self.resultUploadUser = True
        self.resultUploadLFC  = True

        self.countPhEDExQueries = 0
        self.countPhEDExDSQueries = 0
        self.countPhEDExFileQueries = 0

        self.resetCursor()

    def getProcessMemory(self, pid):
        ''' Using pmap to report memory map of a process '''

        process = subprocess.Popen('pmap -x %s | tail -1' % pid, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        process_tuple = process.communicate()
        memory = 0
        if process_tuple[1] == '':
            memory = int(process_tuple[0].split()[2])

        self.logger.info('The memory used by the process with pid %s is %s' % (pid, memory) )
        return memory
        
    def run(self, pid):

        self.logger.info('This process pid %s' % pid)

        short_sleep =  0 # seconds
        long_sleep  =  600 #10 #600 #3600 # seconds 
        i = 1
        while i:

            start_time = datetime.now()
            self.logger.info("lap %d" % i)
 
            self.reset()
        
            newUIDs = self.checkNewUIDs()
            if newUIDs :
                self.logger.info('sleeping for %s s' % short_sleep)
                time.sleep(short_sleep) #just put a delay to allow the consumeToDB to finish possible uploads NB: this is just an additional protection
                self.updateAssociations()
                if self.resultUploadLFC * self.resultUploadUser == True :
                    self.updateLastUID()

            stop_time = datetime.now()
            self.printStats(start_time, stop_time, "time needed to run a lap")

            i += 1

            # check if the memory consumed is too big, in that case kill
            process_memory = self.getProcessMemory(pid)
            if process_memory > MAX_ALLOWED_PROCESS_MEMORY:
                self.logger.error("memory consumption is too big %s respect to the max allowed process memory %s \t going to kill the process %s" % (process_memory, MAX_ALLOWED_PROCESS_MEMORY, pid))
                os.kill(pid, signal.SIGKILL)

            self.logger.info('sleeping for %s s' % long_sleep)
            time.sleep(long_sleep) #sleep for 10 mins, not needed to loop every 5 seconds
                        






