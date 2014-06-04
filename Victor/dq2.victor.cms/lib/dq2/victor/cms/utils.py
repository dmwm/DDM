"""
@copyright: European Organization for Nuclear Research (CERN)
@author: Andrii Thykonov U{andrii.tykhonov@ijs.si<mailto:andrii.tykhonov@ijs.si>}, CERN, 2010-2011
@author: Fernando H. Barreiro U{fernando.harald.barreiro.megino@cern.ch<mailto:fernando.harald.barreiro.megino@cern.ch>}, CERN, 2011
@license: Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at U{http://www.apache.org/licenses/LICENSE-2.0}
"""

from dq2.common import log as logging
from dq2.victor import config

import urllib2, httplib
import simplejson

logger = logging.getLogger("dq2.victor.utils")


class HTTPSClientAuthHandler(urllib2.HTTPSHandler):
    """
    Simple HTTPS client authentication class based on provided
    key/ca information
    """
    def __init__(self, key=None, cert=None, level=0):
        if  level > 1:
            urllib2.HTTPSHandler.__init__(self, debuglevel=1)
        else:
            urllib2.HTTPSHandler.__init__(self)
        self.key = key
        self.cert = cert

    def https_open(self, req):
        """Open request method"""
        #Rather than pass in a reference to a connection class, we pass in
        # a reference to a function which, for all intents and purposes,
        # will behave as a constructor
        return self.do_open(self.get_connection, req)

    def get_connection(self, host, timeout=300):
        """Connection method"""
        if  self.key:
            return httplib.HTTPSConnection(host, key_file=self.key,
                                                cert_file=self.cert)
        return httplib.HTTPSConnection(host)

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

def get_json_data_https(url):
	
    headers = {"Accept": "application/json", "User-Agent": "Victor"}
    req = urllib2.Request(url=url,headers=headers)
    cert = config.get_config('certificate', type='str')
    key = config.get_config('privatekey', type='str')

    opener = urllib2.build_opener(HTTPSClientAuthHandler(cert=cert,key=key))
    f = opener.open(req)
    data = simplejson.load(f)
    f.close()

    if not data:
        logger.critical('Node usage values could not be retrieved from %s'%(url))
        raise Exception('Nodatafound', 'Node usage values could not be retrieved from %s'%(url))

    return data

