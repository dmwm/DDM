"""
Victor class 

@copyright: European Organization for Nuclear Research (CERN)
@author: Andrii Thykonov U{andrii.tykhonov@ijs.si<mailto:andrii.tykhonov@ijs.si>}, CERN, 2010-2011
@author: Fernando H. Barreiro U{fernando.harald.barreiro.megino@cern.ch<mailto:fernando.harald.barreiro.megino@cern.ch>}, CERN, 2011
@license: Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at U{http://www.apache.org/licenses/LICENSE-2.0}
"""

import traceback
import time
import cPickle

from dq2.common import log as logging

from dq2.victor import config
from dq2.victor.siteSelection import SiteSelection
from dq2.victor.replicaReduction import ReplicaReduction
from dq2.victor.notifications import sendErrorMail
from dq2.victor.utils import HOUR, prepareSummary
from dq2.victor.victorDao import VictorDao


class Victor:
    """  
    Class for cleaning agent
    It will monitor sites which have content over total space ratio above some given value
    and clean dataset replicas from these overflowed sites according to algorithm provided in DatasetusageMonitir class                                                                                                                                    
    """  
    
    __logger = logging.getLogger("dq2.victor")                                                                                                                                                               
    __period = HOUR        
    __victorDao = VictorDao()
       
    def __init__(self, name, configFile):
        """                                                                                                                                                                                          
        Initializer for the object.                                                                                                                                                                  
        """
        
        self.__logger.info('Victor starting up...')
                                                        
        self.__siteSelection = SiteSelection()
        self.__replicaReduction = ReplicaReduction()      
            
            
    def run(self):                      
        
        try:
            self.__victorDao.insertRun()
            #Development: Uncomment later       
            fullSiteInfo, accountingSummary = self.__siteSelection.getFullSites()
            #fullSiteInfo = {'SARA-MATRIX_DATADISK': (0.01, 990*(10**12), 1000*(10**12), 0, 0, True, 100**12, 'DATADISK')}
            #fullSiteInfo =      {u'T2_CH_CSCS^b-physics': (-0.19219963159204001, 119219963159204, 100000000000000.0, 0, 0, True, 49219963159204.008, None)}                                                                                                                     #accountingSummary = { u'T2_CH_CSCS^b-physics': {'total': 100000000000000.0, 'tobedeleted': 0, 'used': 119219963159204, 'indeletionqueue': 0, 'newlycleaned': 0}}      

            #fullSiteInfo = {'T2_US_Vanderbilt^heavy-ions': fullSiteInfo['T2_US_Vanderbilt^heavy-ions'], 'T2_BE_UCL^AnalysisOps': fullSiteInfo['T2_BE_UCL^AnalysisOps'],}
            #accountingSummary = {'T2_US_Vanderbilt^heavy-ions': accountingSummary['T2_US_Vanderbilt^heavy-ions'], 'T2_BE_UCL^AnalysisOps': accountingSummary['T2_BE_UCL^AnalysisOps']}
            
            datasetsForSite, successfullycleaned, accountingSummary = self.__replicaReduction.cleanSites(fullSiteInfo, accountingSummary)                            
            prepareSummary(accountingSummary)            
            self.__victorDao.insertAccountingSummary(accountingSummary)
            self.__victorDao.closeRun()
            
        except Exception as e:             
        
            print traceback.format_exc()
            self.__logger.critical(traceback.format_exc())     
            #sendErrorMail('%s\n%s'%(e,traceback.format_exc()))
