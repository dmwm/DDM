"""
DAS query interface based on DAS command line tool by Valentin Kuznetsov
"""
__author__ = "Nicolo Magini"

import logging
import re
import time
import urllib
import urllib2
import platform
import json

logger = logging.getLogger(__name__)

class DASInterface:
    """
    class to fetch records from DAS
    """
    def __init__(self, debug=0):
        self._debug=debug
        if  debug:
            hdlr = urllib2.HTTPHandler(debuglevel=1)
            self.opener = urllib2.build_opener(hdlr)
        else:
            self.opener = urllib2.build_opener()
        header='PopDB API/1.0 (CMS) %s/%s %s/%s (%s)' % (urllib2.__name__,urllib2.__version__,platform.system(),platform.release(),platform.processor())
        self.opener.addheaders = [('User-agent', header)]
        self._PidPattern = re.compile(r'^[a-z0-9]{32}')
        
    def isDasPid(self, data):
        if data and isinstance(data, str) and self._PidPattern.match(data) and len(data) == 32:
            return True
        return False

    def dasRequest(self, url):
        headers = {"Accept": "application/json"}
        req  = urllib2.Request(url=url, headers=headers)
        fdesc = self.opener.open(req)
        data = fdesc.read()
        fdesc.close()
        return data

    def decodeDasData(self,data):
        try:
            dataDict=json.loads(data)
        except ValueError as err:
            logger.error("data from DAS could not be decoded to JSON")
            logger.error(data)
            raise err
        try:
            queryStatus=dataDict['status']
        except KeyError as err:
            logger.error("no status key in DAS record")
            logger.error(data)
            raise err
        if queryStatus == 'ok':
            try:
                if (dataDict['nresults']==0 or not dataDict['data']):
                    logger.warning('query did not return any result')
                    logger.warning(data)
            except KeyError as err:
                logger.error("missing key in DAS record")
                logger.error(data)
                raise err
            return dataDict
        elif queryStatus == 'fail':
            msg='DAS query failed'
            logger.info(msg)
            logger.debug('DAS record:')
            logger.debug(data)
            try:
                msg+=' - Failure reason: \n'+dataDict['reason']+'\n'
            except KeyError:
                msg+='No reason provided'
            raise ValueError(msg)
        else:
            msg='Unrecognized DAS query status: %s' % queryStatus
            raise ValueError(msg)
        
    def get_das_data(self, host, query, idx=0, limit=0):
        """Contact DAS server and retrieve data for given DAS query"""
        params  = {'input':query, 'idx':idx, 'limit':limit}
        path    = '/das/cache'
        pat     = re.compile('http[s]{0,1}://')
        if  not pat.match(host):
            msg = 'Invalid hostname: %s' % host
            raise Exception(msg)
        url = host + path
        encoded_data = urllib.urlencode(params, doseq=True)
        url += '?%s' % encoded_data

        data = self.dasRequest(url)
        
        if self.isDasPid(data):
            pid = data
        else:
            pid = None
        count = 5 # initial waiting time in seconds
        while pid:
            params.update({'pid':data})
            encoded_data = urllib.urlencode(params, doseq=True)
            url  = host + path + '?%s' % encoded_data

            data = self.dasRequest(url)
            
            if self.isDasPid(data):
                pid = data
            else:
                pid = None
            time.sleep(count)
            if  count < 30:
                count *= 2
            else:
                count = 30

        return self.decodeDasData(data)


    
