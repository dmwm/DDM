"""
Replica reduction module: 

@copyright: European Organization for Nuclear Research (CERN)
@author: Andrii Thykonov U{andrii.tykhonov@ijs.si<mailto:andrii.tykhonov@ijs.si>}, CERN, 2010-2011
@author: Fernando H. Barreiro U{fernando.harald.barreiro.megino@cern.ch<mailto:fernando.harald.barreiro.megino@cern.ch>}, CERN, 2011
@license: Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at U{http://www.apache.org/licenses/LICENSE-2.0}
"""

import os
import datetime    

from dq2.common import log as logging
from dq2.victor.datasetSelection import DatasetSelection
from dq2.victor.notifications import sendUncleanedMail
from dq2.victor.utils import GIGA, TERA, TODAY, PATH, dumpInfo, createDirectory, dumpCleaningInfo
from dq2.victor.victorDao import VictorDao

DEBUG_MODE = True

class ReplicaReduction:
    
    __datasetSelection = DatasetSelection()
    __logger = logging.getLogger("dq2.victor.replicaReduction")
    __victorDao = VictorDao()                
                
    def __prepareSummary(self, site, datasets, sizes, creationdates, cpus, naccs, spacesummary, cleaned, nBlocks, maxAccsCont, totalAccsCont):
        self.__logger.info('Going to create the cleaning summary for site %s'%(site))
        dumpCleaningInfo(site, datasets, sizes, creationdates, cpus, naccs, spacesummary, cleaned, nBlocks, maxAccsCont, totalAccsCont)
        self.__victorDao.insertCleaningSummary(site, datasets, sizes, creationdates, cpus, naccs, spacesummary, cleaned, nBlocks, maxAccsCont, totalAccsCont)        
        return

    
    def __clean(self, tobedeleted, refreshed):    
        '''
        @return: True:  all necessary information available
        @return: False: if site is not allowed to be cleaned automatically => shifters should take care of this site
        '''
        if (tobedeleted is None) and (not refreshed):
            return False
        return True   

    
    def __afterAccountingSummary(self, fullSites):
        
        data = {}
        for site in fullSites:
            data[site]={'used_before': used, 'cleaned': spacetoclean, 'used_after': used-spacetoclean, 'total': total}                  
        dumpInfo(data, 'AccountingSummary_cleaning')
        return

    
    def cleanSites(self, fullSites, accountingSummary):
        
        datasets             = {}     
        successfullycleaned  = {} 
        markedfordeletion    = {}
        indeletionqueue_dict = {}
        is_site_refreshed    = {}
        datasets_per_site    = {}
                
        for site in fullSites:
            
            ratio, used, total, tobedeleted, indeletionqueue, refreshed, spacetoclean, spacetoken = fullSites[site]            
                                                                    
            datasetstodelete, spacefordatasets, dates, cleaned, cpus, naccs, cleanedspace, scndspacesummary, nBlocks, maxAccsCont, totalAccsCont = self.__datasetSelection.getDatasetsToDelete(site, spacetoclean, spacetoken)
            
            if cleaned:  
                self.__logger.info   ("Site %s can be successfully cleaned" %site)                                
            else:  
                self.__logger.warning("Site %s could not be cleaned" %site)                
            
            spacesummary               =   [used, total, cleanedspace]
            datasets_per_site[site]    =   [datasetstodelete, spacefordatasets, dates, spacesummary, scndspacesummary, cpus, naccs, nBlocks, maxAccsCont, totalAccsCont]
            markedfordeletion[site]    =   tobedeleted
            indeletionqueue_dict[site] =   indeletionqueue
            successfullycleaned[site]  =   cleaned    
            is_site_refreshed[site]    =   refreshed
            
            accountingSummary[site]['newlycleaned'] = cleanedspace  
                        
        #Mark datasets for deletion
        is_allowed_tobecleaned = {}
        self.__logger.info("Start marking dataset replicas for deletion...")
        for site in datasets_per_site:
            if not self.__clean(markedfordeletion[site], is_site_refreshed[site]):
                self.__logger.info('Site %s is not allowed to be cleaned. No cleaning done!'%site) #in debugging mode
                is_allowed_tobecleaned[site] = False
                continue
            
            is_allowed_tobecleaned[site] = True
            
            if not DEBUG_MODE:
                self.__replicadeletion.markReplicaForDeletion(site, datasets_per_site[site])
                self.__logger.info('Deletion commented out: not marking datasets %s for site %s'%(site)) #in debugging mode
            else:
                self.__logger.info('Dummy mode: not marking datasets for deletion for site %s'%(site)) #in debugging mode
            
            self.__prepareSummary(site, datasets_per_site[site][0], datasets_per_site[site][1], datasets_per_site[site][2], datasets_per_site[site][5], datasets_per_site[site][6], datasets_per_site[site][3], successfullycleaned[site], datasets_per_site[site][7], datasets_per_site[site][8], datasets_per_site[site][9])    
            
        self.__logger.info("Finished marking datasets as ToBeDeleted")                
                
        if not DEBUG_MODE:
            sendUncleanedMail(successfullycleaned)
                
        return datasets, successfullycleaned, accountingSummary
    
    
