"""
Select full sites 

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
from dq2.victor import config
from dq2.victor.factory import create_tool
from dq2.victor.utils import callRetry, dumpInfo, TERA

class SiteSelection:
    
    __logger = logging.getLogger("dq2.victor.siteSelection")     
    __accountingInterface='DQ2AccountingInterface'  
        
    def __init__(self):
                                   
        accountingInterface = config.get_config('accountingInterface', type = str)
        if accountingInterface:
            self.__accountingInterface = accountingInterface           
        
        self.__accounting = create_tool(self.__accountingInterface)
            
                   
    def getFullSites(self):                
                
        sitestoinspect = self.__accounting.getSites()
        fullSiteInfo   = {}
        allInfo = {}
        
        self.__logger.info('Sites to check for full storages: %s' %sitestoinspect)
        #sitestoinspect = sitestoinspect[0:5]
                        
        for site in sitestoinspect:
            self.__logger.debug('Going to evaluate site %s' %(site))
            refreshed = self.__accounting.refreshSiteStatistics(site)                        
            used  = self.__accounting.getUsedSpace(site)
            total = self.__accounting.getTotalSpace(site)   
            tobedeleted = self.__accounting.getToBeDeletedSpace(site)
            indeletionqueue = self.__accounting.getSpaceInDeletionQueue(site)        
            
            allInfo[site]={'used': used, 'total': total, 'tobedeleted': tobedeleted, 'indeletionqueue': indeletionqueue, 'newlycleaned': 0}                
                                 
            if used==None or total==None or total==0:
                self.__logger.warning('Skipped site: %s - Missing values for used and/or pledged space' %(site))
                continue                                  
            
            free = total - used + tobedeleted + indeletionqueue
                        
            ratio = free*1.0/total
                                                 
            self.__logger.info('Accounting Summary. Site: %s - Used: %.2fTB  Free: %.2fTB (%.2f) Total: %.2fTB ToBeDeleted: %.2fTB InDeletionQueue %.2fTB RefreshedStatistics: %s' %(site, used/TERA, free/TERA, ratio, total/TERA, tobedeleted/TERA, indeletionqueue/TERA, refreshed))
            
            if not self.__accounting.isFull(site, ratio, free):            
                self.__logger.debug('Site %s is not full' %(site))
                continue     
            
            spacetoclean, spacetoken = self.__accounting.calculateSpaceToClean(site, used, total, tobedeleted, indeletionqueue)
             
            fullSiteInfo[site] = (ratio, used, total, tobedeleted, indeletionqueue, refreshed, spacetoclean, spacetoken)
            thresholdInfo = self.__accounting.threshold_per_site 
    
        return fullSiteInfo, allInfo
    
