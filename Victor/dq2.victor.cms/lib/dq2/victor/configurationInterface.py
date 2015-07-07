"""
Accounting Interface

@copyright: European Organization for Nuclear Research (CERN)
@author: Fernando H. Barreiro U{fernando.harald.barreiro.megino@cern.ch<mailto:fernando.harald.barreiro.megino@cern.ch>}, CERN, 2011
@license: Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at U{http://www.apache.org/licenses/LICENSE-2.0}
"""

class ConfigurationInterface(object):
    """
    Class representing a Configuration Interface.
    
    @author: Fernando Harald Barreiro Megino <fernando.harald.barreiro.megino@cern.ch>
    """

class Configuration(ConfigurationInterface):
    
    
    def __init__(self, name):
        self.name = name
        
    
    def getSiteProperty(self, site, property):
        return None       
    