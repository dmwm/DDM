"""
@copyright: European Organization for Nuclear Research (CERN)
@author: Fernando H. Barreiro U{fernando.harald.barreiro.megino@cern.ch<mailto:fernando.harald.barreiro.megino@cern.ch>}, CERN, 2011
@license: Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at U{http://www.apache.org/licenses/LICENSE-2.0}
"""

import time
import traceback
import re
import sys
import platform
import datetime

import tempfile
import os

from dq2.common import log as logging
from dq2.victor.popularityInterface import PopularityInterface
from dq2.victor.utils import callRetry, epochTime, dumpTemporaryInfo
from dq2.victor.notifications import sendErrorMail

from utils import get_json_data, get_json_data_https, get_json_data_from_file


"""
host = 'https://cmsweb.cern.ch'
pophost = 'https://cmsweb.cern.ch'
idx = 0
limit = 0
incomplete = '0'
timestart = str(datetime.date.today()-datetime.timedelta(30))
timestop  = str(datetime.date.today())
"""

class PopularityInterface(PopularityInterface):
    """
    Class encapsulating the CMS Popularity Interface.    
    """
    
    __logger = logging.getLogger("dq2.victor.PopularityInterface")
    __MONTH = 30
    __REPLICA_CREATION_DATE_COL=4
    
    
    def __init__(self, name):
        
        #Create a temporary directory to cache information
        self.__tmpdirectory = tempfile.mkdtemp()

                
    def __hasCustodialCopy(self, blockname):
        url='https://cmsweb.cern.ch/phedex/datasvc/json/prod/blockreplicas?custodial=y&complete=y&block=%s'%(blockname)
        url = url.replace('#','%23')
        self.__logger.debug(url)
        replicas = get_json_data(url)
        '''
        replicas = {
            "phedex":{
                "request_version":"2.1.8",
                "request_timestamp":1311755259.31146,
                "instance":"prod",
                "request_call":"blockreplicas",
                "request_url":"http://cmsweb.cern.ch:7001/phedex/datasvc/json/prod/blockreplicas",
                "request_date":"2011-07-27 08:27:39 UTC",
                "block":[
                    {
                        "bytes":"67095800951",
                        "files":"32",
                        "is_open":"n",
                        "name":"/ZJetsToNuNu_Pt-100_7TeV-herwigpp/Summer11-START311_V2-v1/GEN-SIM#7f6b861b-2263-4854-8abf-d096d35d9f1a",
                        "id":"2576551",
                        "replica":[
                            {
                                "bytes":"67095800951",
                                "files":"32",
                                "node":"T1_IT_CNAF_MSS",
                                "time_create":"1311331011",
                                "time_update":"1311610457.398",
                                "group":"DataOps",
                                "node_id":"8",
                                "custodial":"y",
                                "se":"storm-fe-cms.cr.cnaf.infn.it",
                                "subscribed":"y",
                                "complete":"y"}]}],
                "call_time":"0.05906"}}
        '''
        try:
            if replicas['phedex']['block'][0]['replica']:
                return True
        except KeyError:
            self.__logger.warning('Block %s excepted with KeyError. replicas = %s' %(blockname, replicas))
            return False
        except IndexError:
            self.__logger.warning('Block %s excepted with IndexError. replicas = %s' %(blockname, replicas))
            return False
        
        return False

    
    def __getDatasetStats(self, blocks):

        datasetStats = {}
        
        for blockname in blocks:
            datasetName = blockname.split('#')[0]
            
            datasetStats.setdefault(datasetName, {'max': -1, 'sum': 0, 'nblocks': 0})
            
            datasetStats[datasetName]['nblocks'] += 1
            datasetStats[datasetName]['sum']     += int(blocks[blockname]['popularitynacc'])
            if datasetStats[datasetName]['max'] < int(blocks[blockname]['popularitynacc']):
                datasetStats[datasetName]['max']  = int(blocks[blockname]['popularitynacc'])
                
        return datasetStats

            
    def __validateBlock(self, blockname, blockinfo, group, maxnacc, maxcdate):

        if blockinfo['custodial'] != 'n':
            #self.__logger.debug('Refuse because CUSTODIAL')
            return False
        
        if blockinfo['group'] != group:
            #self.__logger.debug('Refuse because we look for replicas from %s and the replica belongs to %s' %(group, blockinfo['group']))
            return False
        
        if blockinfo['popularitynacc'] > maxnacc:
            self.__logger.debug('Refuse because replica has been accessed %s times (>%s)'%(blockinfo['popularitynacc'], maxnacc))
            return False
        
        cdate = datetime.datetime.fromtimestamp(blockinfo['creation_time'])
        cdate_max = datetime.datetime.now() - datetime.timedelta(days=maxcdate)

        if   cdate > cdate_max:
            self.__logger.debug('Refuse because replica is too young %s (>%s)'%(cdate, cdate_max))
            return False
        
        if not self.__hasCustodialCopy(blockname):
            self.__logger.debug('Refuse because replica has no custodial copy')
            return False
        
        return True
        
    
    def __parseUnpopularBlocks(self, site, unpopularBlocks, threshold, creationlimit, physicsgroup):
        
        startdate = unpopularBlocks['popularitytstart']
        enddate = unpopularBlocks['popularitytstop']
        blocks = unpopularBlocks[site]
        blocks_list=[]
        
        datasetStats = self.__getDatasetStats(blocks)
        
        for blockname in blocks:

            datasetname = blockname.split('#')[0]
            
            #Skip custodial blocks, blocks that don't belong to central AnalysisOps and blocks without a custodial copy 
            #if blocks[blockname]['custodial']=='n' and blocks[blockname]['group']=='AnalysisOps' and self.__hasCustodialCopy(blockname):                                            
            if self.__validateBlock(blockname, blocks[blockname], physicsgroup, threshold, creationlimit):     
                try:
                    new_block = (str(blockname), 
                                 int(blocks[blockname]['popularitynacc']), 
                                 None, 
                                 datetime.datetime.fromtimestamp(blocks[blockname]['creation_time']), 
                                 datetime.datetime.fromtimestamp(blocks[blockname]['creation_time']),
                                 int(blocks[blockname]['size']),
                                 int(blocks[blockname]['popularitycpu']),
                                 int(blocks[blockname]['popularitynacc']),
                                 datasetStats[datasetname]['nblocks'],
                                 datasetStats[datasetname]['max'],
                                 datasetStats[datasetname]['sum']
                                 )
                    blocks_list.append(new_block)
                    self.__logger.debug('Appended %s to %s: %s'%(blockname, site, new_block))
                except:
                    self.__logger.error('Error processing block %s for site %s. Complete information: %s' %(blockname, site, blocks[blockname]))
                    continue
            else:
                self.__logger.debug('Refused %s for %s'%(blockname, site))
                #self.__logger.debug('Block %s skipped: custodial %s and group %s' %(blockname, blocks[blockname]['custodial'], blocks[blockname]['group']))
        
        return blocks_list
    
    
    def __getBlocks(self, site):
        
        if os.path.isfile('%s/blocks_%s'%(self.__tmpdirectory, site)):
            unpopularBlocks = get_json_data_from_file('%s/blocks_%s'%(self.__tmpdirectory, site))
            return unpopularBlocks
        
        else:
            url = 'https://cmsweb.cern.ch/popdb/victorinterface/popdbcombine/?sitename=%s' %(site)
            unpopularBlocks = get_json_data_https(url)
            
            dumpTemporaryInfo(unpopularBlocks, self.__tmpdirectory, 'blocks_%s'%(site))      
            return unpopularBlocks 

        
    def getUnpopularDatasets(self, site, lastaccess, threshold, creationlimit, replicatype='secondary'):    
        '''
        Get the list of a site's unpopular block replicas according to the input criteria.
        ''' 
        def compdate(x,y):
            COMPARE_COL=self.__REPLICA_CREATION_DATE_COL
            if   epochTime(x[COMPARE_COL]) > epochTime(y[COMPARE_COL]):
                return 1
            elif epochTime(x[COMPARE_COL]) < epochTime(y[COMPARE_COL]):
                return -1
            else: 
                return 0
            
        site, physicsgroup = site.split('^')  
       
        st=time.time()
        self.__logger.info('Getting unpopular datasets for %s...'%site)                                             
             
        try:                                 
            
            blocks = self.__getBlocks(site)            
            if not blocks or not blocks[site]:                
                raise Exception("Empty answer received from unpopularity API")
                
            unpopularBlocksListed = self.__parseUnpopularBlocks(site, blocks, threshold, creationlimit, physicsgroup)

        except Exception as e:            
            self.__logger.critical('Failed to process site %s [%s - %s]'%(site, e, traceback.format_exc()))
            sendErrorMail('%s\n%s'%(e,traceback.format_exc()))            
            return {} 
        
        finally:
            elapsed = round(time.time()-st, 2)
            self.__logger.info('...back from popDB API for site %s [Took %.2f seconds]'%(site, elapsed))                               
        
        unpopularBlocksListed = sorted(unpopularBlocksListed, compdate)                                                                     
        
        return unpopularBlocksListed
