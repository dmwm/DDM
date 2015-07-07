"""
Accounting Interface

@copyright: European Organization for Nuclear Research (CERN)
@author: Miguel Branco U{miguel.branco@cern.ch<mailto:miguel.branco@cern.ch>}, CERN, 2007-2009
@author: Fernando Barreiro Megino U{fernando.harald.barreiro.meigno@cern.ch<mailto:fernando.harald.barreiro.meigno@cern.ch>}, CERN, 2012
@license: Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at U{http://www.apache.org/licenses/LICENSE-2.0}
"""

import os

from ConfigParser import SafeConfigParser
from threading import Lock

class BadConfigurationError(Exception):
    pass


_config = SafeConfigParser()
try:
    _config.read(['/etc/victormonitoring.cfg'])
except Exception as e:
    raise BadConfigurationError('Could not parse configuration files due to error [%s]' % e)

# configuration objects
_params = {}
_lock = Lock()
    

def get_config(param, type=str, mandatory=False, section='victor'):
    """
    Read setting from configuration file.
    
    @param param: The parameter name to read.
    @param type: If specified, validates against python type.
    @param mandatory: Flag indicating whether parameter must be present.
    @param section: If specified, overrides default configuration file section.
    """
    _lock.acquire()
    try:
        if section in _params and param in _params[section]:
            return _params[section][param]
        value = None
        try:
            value = _config.get(section, param)
        except Exception as e:
            pass
        if not value and mandatory:
            raise BadConfigurationError("Mandatory parameter '%s' missing from configuration file section [%s]" % (param, section))
        try:
            if not value: # empty string is None
                value = None
            elif value and type:
                if type == int:
                    value = int(value)
                    assert(isinstance(value, int))
                elif type == long:
                    value = long(value)
                    assert(isinstance(value, long))
                elif type == bool:
                    value = value.strip()
                    if str(value).upper() in ['ON', 'TRUE', 'T', 'Y', 'YES', '1']:
                        value = True
                    elif str(value).upper() in ['OFF', 'FALSE', 'F', 'N', 'NO', '0']:
                        value = False
                    assert(isinstance(value, bool))                    
                elif type == str:
                    value = value.strip()
                    assert(isinstance(value, str))
                elif type == float:
                    value = float(value)
                    assert(isinstance(value, float))
                elif type == list or type=='list_2':
                    value = value.strip().split(',')
                    assert(isinstance(value, list))
                    value=map(lambda x: x.strip(), value)
                    while True:
                        try: value.remove('')
                        except ValueError: break
                                
        except Exception as e:
            raise BadConfigurationError('Error reading parameter from configuration file [%s]' % param)
        _params.setdefault(section, {})
        _params[section][param] = value
        return value
    finally:
        _lock.release()