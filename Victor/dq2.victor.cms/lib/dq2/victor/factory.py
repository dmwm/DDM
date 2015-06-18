"""
Dataset selection 

@copyright: European Organization for Nuclear Research (CERN)
@author: Fernando H. Barreiro U{fernando.harald.barreiro.megino@cern.ch<mailto:fernando.harald.barreiro.megino@cern.ch>}, CERN, 2011
@license: Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at U{http://www.apache.org/licenses/LICENSE-2.0}
"""

from dq2.victor import config

def create_tool(tool):
    """
    Create an instance of a tool.
    
    Reads configuration file based on a section:
    
    [plugin-<tool>]
    module=<python module>
    class=<python class>
    
    @param tool: The tool identifier.    
    @return: Instance of a tool.
    """
    try:    
        section = 'plugin-%s' % tool
        modname = config.get_config('module',  str, section=section, mandatory=True)
        clsname = config.get_config('class',  str, section=section, mandatory=True)
        
        mod = __import__(modname)
        comp = modname.split('.')
        for c in comp[1:]:
            mod = getattr(mod, c)
        
        return getattr(mod, clsname)(section)
    except Exception as e:
        raise Exception ('Unable to initialize plug-in %s [%s]' % (tool, e))
