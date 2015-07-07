"""
Dataset selection 

@copyright: European Organization for Nuclear Research (CERN)
@author: Andrii Thykonov U{andrii.tykhonov@ijs.si<mailto:andrii.tykhonov@ijs.si>}, CERN, 2010-2011
@author: Fernando H. Barreiro U{fernando.harald.barreiro.megino@cern.ch<mailto:fernando.harald.barreiro.megino@cern.ch>}, CERN, 2011
@license: Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at U{http://www.apache.org/licenses/LICENSE-2.0}
"""

import time
import traceback

from dq2.common import log as logging

from dq2.victor import config
from dq2.victor.utils import castListToIntegers, epochTime 
from dq2.victor.factory import create_tool

 
class DatasetSelection:      
    
    __logger = logging.getLogger("dq2.victor.datasetSelection")
    __popularityInterface = 'DQ2PopularityInterface'
    
    MONTH = 30
    
    # Algorithm 1. Default cleaning algorithm
    #__thresholds = [{'threshold' : 1, 'lastaccess' : [3, 2, 1]}]
    __thresholds = [{'threshold' : 1, 'lastaccess' : [1]}]
    __creationlimit = 90  #days
    
    # Algorithm 2. User spacetokens and similar. Delete by replica creation date 
    __algorithm2_custodiality  ='default' 
    __algorithm2_spacetokens   =[]  #'SCRATCHDISK']    
    __algorithm2_creationlimit ={}  #{'SCRATCHDISK':15, 'PRODDISK':31}
    
    #Positions of 
    __DATASET_NAME_COL          = 0
    __LASTACCESS_COL            = 2   
    __DATASET_CREATION_DATE_COL = 3
    __REPLICA_CREATION_DATE_COL = 4
    __DATASET_SIZE_COL          = 5
    __CPU_COL                   = 6
    __NACC_COL                  = 7
    __NBLOCKS_COL               = 8
    __NMAX_COL                  = 9
    __NTOTAL_COL                = 10
            
    
    def __init__(self):
        
        popularityInterface = config.get_config('popularityInterface', type = str)
        if popularityInterface:
            self.__popularityInterface = popularityInterface           
        
        self.__popularity = create_tool(self.__popularityInterface)
               
        creationlimit = config.get_config('creationlimit', int)        
        if creationlimit is not None:
            self.__creationlimit = creationlimit     
        
        thresholds = config.get_config('thresholds', list)
        lastaccess= config.get_config('lastaccess', 'list_2')
        
        is_parsed=self.__parseThresholds__(thresholds, lastaccess)
        if is_parsed:
            self.__logger.info('Successfully parsed the thresholds: %s'%str(self.__thresholds))
        else:
            self.__logger.error('Failed to parse thresholds from configuration file. Using default ones: %s'%str(self.__thresholds))
        
        # parse algorithm2 parameters
        algorithm2_spacetokens   = config.get_config('algorithm2_spacetokens', list)
        if algorithm2_spacetokens is None:
            algorithm2_spacetokens = []
        algorithm2_creationlimit = config.get_dict  ('algorithm2_creationlimit', type='positive_int')        
        self.__algorithm2_spacetokens, self.__algorithm2_creationlimit = self.__verifyAlgorithm2param(algorithm2_spacetokens,
                                                                                                       algorithm2_creationlimit)
        self.__logger.debug('Algorithm2_spacetokens   : %s'%self.__algorithm2_spacetokens)
        self.__logger.debug('Algorithm2_creationlimit : %s'%self.__algorithm2_creationlimit)
         
         
    def __verifyAlgorithm2param(self, algorithm2_spacetokens, algorithm2_creationlimit):
        spacetokens   = []
        creationlimit = {}
        for token in algorithm2_spacetokens:            
            if not token in algorithm2_creationlimit: 
                self.__logger.warning('Algorithm2: %s is in spacetoken list, but with invalid or absent parameter info'%token)
                self.__logger.warning('Algorithm2: %s - using default algorithm instead'%token)
            else:
                spacetokens.append(token)
                creationlimit[token]=algorithm2_creationlimit[token]
        return spacetokens, creationlimit                   
                 
        
    def __parseThresholds__(self, thresholds, lastaccess):
        
        if thresholds is None:
            return None
        try:
            threshold_list=[]
            
            for i in xrange(len(thresholds)):
                cur_threshold={
                               'threshold'  :  int(thresholds[i]),
                               'lastaccess' :  sorted(castListToIntegers(lastaccess[i]), reverse=True)
                               }
                threshold_list.append(cur_threshold)                 
        
        except Exception:
            self.__logger.error('Failed to parse thresholds from configuration file')                 
            self.__logger.info(traceback.format_exc())
            return None
        
        self.__thresholds=threshold_list           
        return True
    
    
    def __appendDatasets(self, datastetsToCheck, oldDatasets):
        '''
        this function filters out from datastetsToCheck the datasets, 
        which are already present in oldDatasets
        and return a filtered list of datasets (newDatasets)
        '''
        newDatasets=[]        
        for data in datastetsToCheck:
            ######## check if dataset is already in the list 
            if data[self.__DATASET_NAME_COL] not in oldDatasets:
                ######## check if one dataset is included few times in one set
                if data in newDatasets:
                    text='Duplicate dataset:%s returned for site'%data[self.__DATASET_NAME_COL]
                    self.__logger.warning(text)
                    continue    
                            
                newDatasets.append(data)                
        return newDatasets    
    
        
    def __filterDatasetsToDelete(self, site, spacetoclean, datasetsinfo):   
        '''
        It takes datasets from datasetsinfo and append it to deletion queue (datasetstodelete),
        while targetspace is not reached/ or the end of datasetsinfo is reached
        '''
        datasetstodelete = []
        spacefordataset  = []
        dates            = []
        naccs            = []
        cputimes         = []
        nBlocks          = []
        maxAccsCont      = []
        totalAccsCont    = []
                                
        cleanedspace=0
        cleaned=False                              
        
        for data in datasetsinfo:      
            cur = data[self.__DATASET_SIZE_COL]
            if not isinstance(cur, int):       
                self.__logger.info('Dataset: %s has invalid DATASETSIZE attribute: %s'%(data[self.__DATASET_NAME_COL], str(cur)))
                self.__logger.info('Invoking alternative method to calculate dataset size...')
                cur=self.__getreplicasize(data[self.__DATASET_NAME_COL])
                if not isinstance(cur, int): 
                    continue                
                self.__logger.info('The size of dataset is: %d Bytes'%cur)      
            
            cleanedspace += cur
                        
            datasetstodelete += [data[self.__DATASET_NAME_COL]]                
            dt = data[self.__REPLICA_CREATION_DATE_COL]                    
            dates += [epochTime(dt)]         
            spacefordataset += [cur]
            if len(data) > self.__DATASET_SIZE_COL:
                naccs += [data[self.__NACC_COL]]
                cputimes += [data[self.__CPU_COL]]
                nBlocks       += [data[self.__NBLOCKS_COL]]
                maxAccsCont   += [data[self.__NMAX_COL]]
                totalAccsCont += [data[self.__NTOTAL_COL]]
            else:
                naccs += [None]
                cputimes += [None]
                nBlocks       += [None]
                maxAccsCont   += [None]
                totalAccsCont += [None]
                                            
            if cleanedspace >= spacetoclean:
                cleaned=True
                break            
                            
        return datasetstodelete, spacefordataset, dates, cleaned, cleanedspace, cputimes, naccs, nBlocks, maxAccsCont, totalAccsCont
   
    
    def getSecondarySpace(self, site):
        return self.__getSpaceForDatasets(site, 0, 1e6, 0)
    
    
    def getOldSecondarySpace(self, site):
        
        return self.__getSpaceForDatasets(site, 0, 1e6, self.__creationlimit)
    
    
    def __getSpaceForDatasets(self, site, lastaccess, threshold, creationlimit):   
             
        secondarydatasets = self.__popularity.getUnpopularDatasets(site, lastaccess, threshold, creationlimit) 
        space=0
        for data in secondarydatasets:       
            cur = data[self.__DATASET_SIZE_COL]
            if not isinstance(cur, int):       
                self.__logger.info('Dataset: %s has invalid DATASETSIZE attribute: %s'%(data[self.__DATASET_NAME_COL], str(cur)))
                self.__logger.info('Invoking alternative method to calculate dataset size...')
                cur = self.__getreplicasize(data[self.__DATASET_NAME_COL])
                if not isinstance(cur, int): 
                    continue                
                self.__logger.info('The size of dataset is: %d Bytes'%cur)                 
            space+=cur                       
        return space 
    

    def __getDatasetsToDeleteAlgorithm2(self, site, spacetoclean, spacetoken):
        threshold=1e12
        lastaccess=0
        creationlimit = self.__algorithm2_creationlimit[spacetoken] #days
        replicatype   = self.__algorithm2_custodiality  #'default'
                
        datasets=self.__popularity.getUnpopularDatasets(site, lastaccess=lastaccess, threshold=threshold, creationlimit=creationlimit, replicatype=replicatype)                       
        datasetstodelete, spacefordataset, dates, cleaned, cleanedspace, cputimes, naccs, nBlocks, maxAccsCont, totalAccsCont = self.__filterDatasetsToDelete(site, spacetoclean, datasets)
        return datasetstodelete, spacefordataset, dates, cleaned, cleanedspace, cputimes, naccs, nBlocks, maxAccsCont, totalAccsCont    
        

    def __getDatasetsToDeleteStandard(self, site, spacetoclean):
        cleaned=False
        totalcleaned=0        
        
        datasetstodeleteTotal=[]
        spacefordatasetTotal=[]
        datesTotal=[]   
        for threshold_set in self.__thresholds:
            threshold=threshold_set['threshold']            
            for lastaccess in threshold_set['lastaccess']:  
                self.__logger.debug('Threshold: %d Lastaccess: %d'%(threshold, lastaccess))             
                datasets = self.__popularity.getUnpopularDatasets(site, lastaccess=lastaccess, threshold=threshold, creationlimit=self.__creationlimit)                                
                datasets = self.__appendDatasets(datasets, datasetstodeleteTotal)                
                datasetstodelete, spacefordataset, dates, cleaned, cleanedspace, cputimes, naccs, nBlocks, maxAccsCont, totalAccsCont = self.__filterDatasetsToDelete(site, spacetoclean, datasets)
                
                totalcleaned          += cleanedspace
                datasetstodeleteTotal += datasetstodelete
                spacefordatasetTotal  += spacefordataset
                datesTotal+=dates
                
                if cleaned: 
                    break
            if cleaned: 
                break
            
        return datasetstodeleteTotal, spacefordatasetTotal, datesTotal, cleaned, totalcleaned, cputimes, naccs, nBlocks, maxAccsCont, totalAccsCont


    def getDatasetsToDelete(self, site, spacetoclean, spacetoken):
        
        #Alternative algorithm for SCRATCHDISK
        if spacetoken in self.__algorithm2_spacetokens:     
            
            datasetstodelete, spacefordataset, dates, cleaned, cleanedspace, cputimes, naccs, nBlocks, maxAccsCont, totalAccsCont = self.__getDatasetsToDeleteAlgorithm2(site, spacetoclean, spacetoken)
            return datasetstodelete, spacefordataset, dates, cleaned, cputimes, naccs, cleanedspace, None, nBlocks, maxAccsCont, totalAccsCont 
        
        #Default algorithm for DATADISK            
        else:                                                
        
            datasetstodelete, spacefordataset, dates, cleaned, cleanedspace, cputimes, naccs, nBlocks, maxAccsCont, totalAccsCont = self.__getDatasetsToDeleteStandard(site, spacetoclean)
            if cleaned:
                return datasetstodelete, spacefordataset, dates, cleaned, cputimes, naccs, cleanedspace, None, nBlocks, maxAccsCont, totalAccsCont
            else:
                self.__logger.info   ("Getting space for secondary datasets for site %s....." %site) 
                totalscnd        = self.getSecondarySpace(site)
                oldscnd          = self.getOldSecondarySpace(site)
                scndspacesummary = [totalscnd, oldscnd]            
                self.__logger.info   ("Finished with secondary datasets site %s....." %site)                
                return datasetstodelete, spacefordataset, dates, cleaned, cputimes, naccs, cleanedspace, scndspacesummary, nBlocks, maxAccsCont, totalAccsCont
            
 
