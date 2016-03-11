"""
@copyright: European Organization for Nuclear Research (CERN)
@author: Andrii Thykonov U{andrii.tykhonov@ijs.si<mailto:andrii.tykhonov@ijs.si>}, CERN, 2010-2011
@author: Fernando H. Barreiro U{fernando.harald.barreiro.megino@cern.ch<mailto:fernando.harald.barreiro.megino@cern.ch>}, CERN, 2011
@license: Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at U{http://www.apache.org/licenses/LICENSE-2.0}
"""
from __future__ import absolute_import


from .notifications import send_mail

class DQ2DeletionInterface(DeletionInterface):
    """
    Class encapsulating the ATLAS DDM Deletion Interface.    
    """
    __logger = logging.getLogger("dq2.victor.DeletionInterface")
    
    #TO BE REPLACED BY A DICTIONARY OF SITE CONTACTS OR IMPLEMENT A METHOD THAT GETS THESE ADDRESSES DINAMICALLY
    recipients = ['fernando.harald.barreiro.megino@cern.ch', 'daniele.spiga@cern.ch', 'domenico.giordano@cern.ch', 'nicolo.magini@cern.ch']    
    sender = 'fbarreir@cern.ch'

    
    def __init__(self, name):
        
        self.__deletions={}        
        

    def markReplicaForDeletion(self, site, block):     

        self.__deletions.setdefault(site, [])
        self.__deletions[site].append(block)                           
        self.__logger.info('Appended block %s for deletion in site %s'%(block, site))
        
    
    def closeDeletion(self):
        
        for site in self.__deletions:
            text = '\n'.join(deletions[site])
            subject = "[VICTOR NOTIFICATION] Blocks to be deleted for %s"%(site)            
            send_mail(text, recipients, sender, subject)
            self.__logger.info('Deletion mail sent for %'%(site))
        
            
            

