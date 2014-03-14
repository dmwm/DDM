"""
Accounting Interface

@copyright: European Organization for Nuclear Research (CERN)
@author: Fernando H. Barreiro U{fernando.harald.barreiro.megino@cern.ch<mailto:fernando.harald.barreiro.megino@cern.ch>}, CERN, 2011-?
@license: Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at U{http://www.apache.org/licenses/LICENSE-2.0}
"""


from dq2.victor import config


class AccountingInterface(object):
    """
    Class representing an Accounting Interface.
    
    @author: Fernando Harald Barreiro Megino <fernando.harald.barreiro.megino@cern.ch>
    """
    
    def getSites(self, spacetokens):    
        """        
        @return: List with all the sites with spacetoken type        
        """
        return []
    
    def getUsedSpace(self,site):
        return 0
    
        
    def getTotalSpace(self,site):            
        return 0
        
    
    def getToBeDeletedSpace(self,site):
        return 0        
        
        
    def refreshSiteStatistics(self,site):            
        return True
        
    
    def getSpaceInDeletionQueue(self,site):
        return 0
        
        

class Accounting(AccountingInterface):
        
    def __init__(self, name):
        self.name = name
        
        