"""
@copyright: European Organization for Nuclear Research (CERN)
@author: Andrii Thykonov U{andrii.tykhonov@ijs.si<mailto:andrii.tykhonov@ijs.si>}, CERN, 2010-2011
@author: Fernando H. Barreiro U{fernando.harald.barreiro.megino@cern.ch<mailto:fernando.harald.barreiro.megino@cern.ch>}, CERN, 2011
@license: Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at U{http://www.apache.org/licenses/LICENSE-2.0}
"""

from dq2.common import log as logging

import urllib2
import simplejson

logger = logging.getLogger("dq2.victor.utils")


def get_json_data_from_file(file):

    f = open(file)
    data = simplejson.load(f)
    f.close()
    
    if not data:
        logger.critical('Node usage values could not be retrieved from %s'%(url))
        raise Exception('Nodatafound', 'Node usage values could not be retrieved from %s'%(url))
    
    return data

    
def get_json_data(url):

    req = urllib2.Request(url)

    opener = urllib2.build_opener()
    f = opener.open(req)
    data = simplejson.load(f)
    f.close()
    
    if not data:
        logger.critical('Node usage values could not be retrieved from %s'%(url))
        raise Exception('Nodatafound', 'Node usage values could not be retrieved from %s'%(url))
    
    return data


def get_json_data_improper(url):
    """
    Same as get_json_data but replaces single quotes by double quotes in case the file is malformed
    """     

    req = urllib2.Request(url)
    
    opener = urllib2.build_opener()
    f = opener.open(req)
    data_s=f.read()
    f.close()
    
    data_s=data_s.replace("'", '"')
    
    data = simplejson.loads(data_s)
    if not data:
        logger.critical('Node usage values could not be retrieved from %s'%(url))
        raise Exception('Nodatafound', 'Node usage values could not be retrieved from %s'%(url))
    
    return data      
