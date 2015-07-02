"""
Accounting Interface

@copyright: European Organization for Nuclear Research (CERN)
@author: Miguel Branco U{miguel.branco@cern.ch<mailto:miguel.branco@cern.ch>}, CERN, 2007-2009
@author: Andrii Thykonov U{andrii.tykhonov@ijs.si<mailto:andrii.tykhonov@ijs.si>}, CERN, 2010-2011
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
    _config.read(['%s/etc/dq2.cfg' % os.environ.get('DQ2_HOME'),
                  os.path.expanduser('~/.dq2/etc/dq2.cfg'),
                  '/opt/dq2/etc/dq2.cfg'])
except Exception as e:
    raise BadConfigurationError('Could not parse configuration files due to error [%s]' % e)

# configuration objects
_params = {}
_lock = Lock()
    

def get_config(param, type=str, mandatory=False, section='dq2-victor'):
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
                    value=map(lambda x: x.strip(),value)
                    while True:
                        try: value.remove('')
                        except ValueError: break
                                
                #######################################
                if type == 'list_2':
                    for i in range(len(value)):
                        value[i] = value[i].strip().split(';')
                        assert(isinstance(value[i], list))
                        while True:
                            try: value[i].remove('')
                            except ValueError: break                        
                ######################################## 
                
                           
                    
        except Exception as e:
            raise BadConfigurationError('Error reading parameter from configuration file [%s]' % param)
        _params.setdefault(section, {})
        _params[section][param] = value
        return value
    finally:
        _lock.release()


def __convertToDictionary(stringTuple,valueParser):
        
    dict={}
    for string in stringTuple:
        key,value=string.split(':')
        key=key.strip()
        #value=float(value)
        value=valueParser(value)
        if not value: continue
        
        dict[key]=value
    
    return dict


def __parseFloat(pvalue):    
    try:
        value=float(pvalue)
        return value
    except:
        return None
    
def __parsePositiveInt(pvalue):
    try:
        value=int(pvalue)
        if value<0:return  None
        return             value
    except:
        return             None
            
    
def __parseSize(pvalue):
    TERA='TB'
    
    pvalue=pvalue.strip()    
    if pvalue.endswith(TERA):
        pvalue=pvalue[:pvalue.rfind(TERA)]
        value=__parseFloat(pvalue) 
        if value: value=value*(10**12)
        return value
    else:
        return __parseFloat(pvalue)


def get_dict(configParam,type=None ,section='dq2-agents-diskspacemonitor'):
    cfgdict = get_config(configParam, list, section = section)   
    
    if cfgdict is None:
        return None
     
    if   type =='size':
        cfgdict = __convertToDictionary(cfgdict,__parseSize)
    elif type =='positive_int':
        cfgdict = __convertToDictionary(cfgdict,__parsePositiveInt)
    else:
        cfgdict = __convertToDictionary(cfgdict,__parseFloat)
    
    return cfgdict

    


