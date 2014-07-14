"""
Database library for Victor 

@copyright: European Organization for Nuclear Research (CERN)
@author: Fernando H. Barreiro U{fernando.harald.barreiro.megino@cern.ch<mailto:fernando.harald.barreiro.megino@cern.ch>}, CERN, 2011
@license: Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at U{http://www.apache.org/licenses/LICENSE-2.0}
"""

import cx_Oracle
import traceback
from datetime import datetime
from dq2.victor import config
from dq2.common import log as logging
from dq2.victor.utils import GIGA, TERA, PETA

class VictorDao:    
    
    
    def __init__(self):

        user           = config.get_config('db_user', type='str')
        password       = config.get_config('db_password', type='str')
        connectionName = config.get_config('db_conn', type='str')
        if not user or not password or not connectionName:
            raise Exception, 'No DB connection specified in configuration file'
        
        connection_string = '%s/%s@%s'%(user, password, connectionName)
        self.__connection = cx_Oracle.Connection(connection_string)
        self.__logger = logging.getLogger('dq2.victor.victorDao')

    
    def insertRun(self):
        
        cursor = cx_Oracle.Cursor(self.__connection)    
        try:
            #query = "INSERT INTO CMS_CLEANING_AGENT.t_run (runDate) VALUES(SYSDATE)"
            query = "INSERT INTO t_run (runDate, runId) VALUES(SYSDATE, SEQ_RUN.NEXTVAL)"                
            cursor.execute(query)
            self.__connection.commit()
            self.__logger.info('Inserted a new run')
        except:
            self.__logger.critical('Unable to insert a new run: %s'%traceback.format_exc())
        finally:
            cursor.close()
            return
        
        
    def closeRun(self):
        
        cursor = cx_Oracle.Cursor(self.__connection)    
        try:
            query = "UPDATE t_run SET finished = 1 WHERE runId = (SELECT MAX(runId) FROM t_run)" 
            cursor.execute(query)
            self.__connection.commit()
            self.__logger.info('Closed ongoing run')
        except:
            self.__logger.critical('Unable to close ongoing run: %s'%(traceback.format_exc()))
        finally:
            cursor.close()
            return
    
    
    def getRun(self):
        
        cursor = cx_Oracle.Cursor(self.__connection)
        runId = None    
        try:    
            query = "SELECT MAX(runId) FROM t_run WHERE finished = 0"
            cursor.execute(query)    
            runId = cursor.fetchone()[0]      
            self.__logger.info('Got latest run %d' %runId)  
        except:
            self.__logger.critical('Unable to get the runId: %s'%traceback.format_exc())
        finally:
            cursor.close()
            return int(runId)
    
    
    def insertRunSite(self, rundId, siteName):
        
        cursor = cx_Oracle.Cursor(self.__connection)    
        try:
            query = "INSERT INTO t_run_site (runId, siteName) VALUES(:runId, :siteName)"
            bindVar={'runId': runId, 'siteName': siteName}
            cursor.execute(query, bindVar)
            self.__connection.commit()
            self.__logger.info('Inserted runSite %d-%s' %(runId, siteName))
        except:
            self.__logger.critical('Unable to insert a new run-site entry: %s'%traceback.format_exc())
        finally:
            cursor.close()
            return 
    
    
    def insertAccountingRecord(self, rundId, siteName, total, used, toBeDeleted, inDeletionQueue, newlyCleaned):
        
        cursor = cx_Oracle.Cursor(self.__connection)    
        try:
            query = '''
                     INSERT INTO t_accounting_record (runId, siteName, total, used, toBeDeleted, inDeletionQueue, newlyCleaned) 
                     VALUES(:runId, :siteName, :total, :used, :toBeDeleted, :inDeletionQueue, :newlyCleaned)
                     '''
            bindVar={'runId': runId, 'siteName': siteName, 'total': total, 'used': used, 'toBeDeleted': toBeDeleted, 'inDeletionQueue': inDeletionQueue, 'newlyCleaned': newlyCleaned}
            cursor.execute(query, bindVar)
            self.__connection.commit()
            self.__logger.info('Inserted accounting record for %s' %(siteName))
        except:
            self.__logger.critical('Unable to insert a new accounting record: %s'%traceback.format_exc())
        finally:
            cursor.close()
            return
    
    
    def insertCleanedDataset(self, rundId, siteName, dsn, cont, rcdate, dsSize, nAcc, cpuTime):
        
        cursor = cx_Oracle.Cursor(self.__connection)    
        try:
            query = '''
                     INSERT INTO t_cleaned_dataset (runId, siteName, dsn, cont, rcdate, dsSize, nAcc, cpuTime) 
                     VALUES(:runId, :siteName, :dsn, :cont, :rcdate, :dsSize, :nAcc, :cpuTime)
                     '''
            bindVar={'runId': runId, 'siteName': siteName, 'dsn': dsn, 'cont': cont, 'rcdate': rcdate, 'dsSize': dsSize, 'nAcc': nAcc, 'cpuTime': cpuTime}
            cursor.execute(query, bindVar)
            self.__connection.commit()
            self.__logger.info('Inserted cleaned dataset %s for %s' %(dsn, siteName))
        except:
            self.__logger.critical('Unable to insert a new cleaned replica: %s'%traceback.format_exc())
        finally:
            cursor.close()
            return
        
        
    def insertCleaningSummary(self, site, datasets, sizes, creationdates, cpus, naccs, spacesummary, cleaned, nBlocks, maxAccsCont, totalAccsCont):
        
        if not datasets:
            return
        
        siteInfo = []
        site = str(site)        
         
        for dataset, size, cdate, cpu, nacc, nBlock, maxAccCont, totalAccCont in zip(datasets, sizes, creationdates, cpus, naccs, nBlocks, maxAccsCont, totalAccsCont):
            
            #CMS specific
            if '#' in dataset:
                cont = str(dataset).split('#')[0]
            else:
                cont = None             
            
            if cpu is not None:
                cpu = int(cpu)
            if nacc is not None:
                nacc = int(nacc)
               
            siteInfo.append({'dsn': str(dataset), 'cont': cont, 'dsSize': size, 'rcdate': datetime.fromtimestamp(cdate), 'cpuTime': cpu, 'nAcc': nacc, 'nBlock': nBlock, 'maxAccCont': maxAccCont, 'totalAccCont': totalAccCont})
        
        run = self.getRun()
        
        cursor = cx_Oracle.Cursor(self.__connection)
            
        try:
            try:
                query = "INSERT INTO t_run_site (runId, siteName) VALUES(:runId, :siteName)"
                bindVar={'runId': run, 'siteName': site}
                cursor.execute(query, bindVar)
                self.__connection.commit()
                self.__logger.info('Inserted runSite %d-%s in insertCleaningSummary' %(run, site))
            except cx_Oracle.IntegrityError:
                pass            

            query = """
                     INSERT INTO t_cleaned_dataset (runId, siteName, dsn, cont, rcdate, dsSize, nAcc, cpuTime, nBlock, maxAccsCont, totalAccsCont) 
                     VALUES(%s, \'%s\', :dsn, :cont, :rcdate, :dsSize, :nAcc, :cpuTime, :nBlock, :maxAccCont, :totalAccCont)
                     """%(run, site)
            
            cursor.executemany(query, siteInfo)
            self.__connection.commit()
            self.__logger.info('Inserted cleaning summary for %s' %(site))
        except:
            self.__logger.critical('Unable to insert cleaned replica bulk: %s \nsiteInfo=%s'%(traceback.format_exc(), siteInfo))            
        finally:
            cursor.close()
            return        
        

    def insertAccountingSummary(self, data):
    
        siteInfo = []
        sites=data.keys()
        
        run = self.getRun()
        
        cursor = cx_Oracle.Cursor(self.__connection)            
        
        for site in sites:
            
            if data[site]['used']:
                used = data[site]['used']
            else:
                used = None
            if data[site]['total']:
                total = data[site]['total']
            else:
                total = None
            if data[site]['tobedeleted']:
                tobedeleted = data[site]['tobedeleted']
            else:
                tobedeleted = None
            if data[site]['indeletionqueue']:
                indeletionqueue = data[site]['indeletionqueue']
            else:
                indeletionqueue = None
            if data[site]['newlycleaned']:
                newlycleaned = data[site]['newlycleaned']
            else:
                newlycleaned = None
                
            try:
                query = "INSERT INTO t_run_site (runId, siteName) VALUES(:runId, :siteName)"
                bindVar={'runId': run, 'siteName': site}                
                cursor.execute(query, bindVar)
                self.__connection.commit()
                self.__logger.info('Inserted runSite for %s'%site)
            except cx_Oracle.IntegrityError:
                pass
        
            siteInfo.append({'runId': run, 'site': site, 'used': used, 'total': total, 'tobedeleted': tobedeleted, 'indeletionqueue': indeletionqueue, 'newlycleaned': newlycleaned})        
        
        try:
 
            query = '''
                     INSERT INTO t_accounting_record (runId, siteName, total, used, toBeDeleted, inDeletionQueue, newlyCleaned) 
                     VALUES(:runId, :site, :total, :used, :tobedeleted, :indeletionqueue, :newlycleaned)
                     '''
            
            cursor.executemany(query, siteInfo)
            self.__connection.commit()
            self.__logger.info('Inserted accounting summary for all sites')

        except:
            self.__logger.critical('Unable to insert accounting records: %s\n\n%s'%(siteInfo, traceback.format_exc()))
        finally:
            cursor.close()
            return        
        
