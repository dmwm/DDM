"""
PHEDEX query interface based on PHEDEX command line tool by Valentin Kuznetsov
"""

import logging
import re
import time
import urllib
import urllib2
import platform
import json
import yaml

logger = logging.getLogger(__name__)

class PHEDEXInterface:
    """
    class to fetch records from PHEDEX
    """
    def __init__(self, debug=0):
        self._debug=debug
        if  debug:
            hdlr = urllib2.HTTPHandler(debuglevel=1)
            self.opener = urllib2.build_opener(hdlr)
        else:
            self.opener = urllib2.build_opener()
        header='XRootDMon API/1.0 (CMS) %s/%s %s/%s (%s)' % (urllib2.__name__,urllib2.__version__,platform.system(),platform.release(),platform.processor())
        self.opener.addheaders = [('User-agent', header)]
        self._PidPattern = re.compile(r'^[a-z0-9]{32}')
        

    def phedexRequest(self, url):
        headers = {"Accept": "application/json"}
        req  = urllib2.Request(url=url, headers=headers)
        fdesc = self.opener.open(req)
        data = fdesc.read()
        fdesc.close()
        return data

    def getDataSetsData(self,val,listData):
        for ds in val['dataset']:
            dname=ds['name']
            for block in ds['block']:
                bname=block['name']
                for file in block['file']:
                    lfn=file['lfn']
                    #listData.append({'dataset':dname,'block':bname,'file':lfn})
                    listData.append((dname,bname,lfn))
                    

    def decodePhedexData(self,data):
        try:
            #dataDict=json.loads(data)
            dataDict=yaml.load(data)
        except ValueError as err:
            logger.error("data from PHEDEX could not be decoded to JSON")
            logger.error(data)
            raise err
        try:
            phedexData=dataDict['phedex']                
        except KeyError as err:
            logger.error("no phedex key in PHEDEX record")
            logger.error(data)
            raise err

        try:
            dbsData=phedexData['dbs']
        except KeyError as err:
            logger.error("no dbs key in PHEDEX record")
            logger.error(data)
            raise err

        listData=[]
        for val in dbsData:
            self.getDataSetsData(val,listData)

        return listData
    
                
    def get_phedex_data(self, host, query):
        """Contact PHEDEX server and retrieve data for given PHEDEX query"""
        path     = '/phedex/datasvc/json/prod/data'
        pat     = re.compile('http[s]{0,1}://')
        if  not pat.match(host):
            msg = 'Invalid hostname: %s' % host
            raise Exception(msg)
        url = host + path

                
        url += '?%s' % query.replace("#","%23")
        logger.debug('\nrequest url\n %s' % url )

        data = self.phedexRequest(url)

        #print '\nreturned data from phedex\n' , data
        return self.decodePhedexData(data)


    
