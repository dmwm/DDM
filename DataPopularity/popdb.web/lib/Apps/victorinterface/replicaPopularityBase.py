__author__ = "Nicolo Magini"

import logging
import re
import json
import urllib
import urllib2
import platform
import datetime
from Apps.popCommon.utils.dasInterface.dasInterface import DASInterface
from Apps.popCommon.utils import Lexicon
from Apps.popCommon.utils.confSettings import confSettings
from Apps.popCommon.PopularityException import PopularityConfigException

logger = logging.getLogger(__name__)

class ReplicaPopularity:
    """
    class to fetch block replica information from DAS and PopDB and combine
    """
    def __init__(self, debug=0,dasHost='https://cmsweb.cern.ch',popHost='http://cms-popularity-prod.cern.ch'):
        self._debug = debug
        if  debug:
            hdlr = urllib2.HTTPHandler(debuglevel=1)
            self.opener = urllib2.build_opener(hdlr)
        else:
            self.opener = urllib2.build_opener()
        header='PopDB API/1.0 (CMS) %s/%s %s/%s (%s)' % (urllib2.__name__,urllib2.__version__,platform.system(),platform.release(),platform.processor())
        self.opener.addheaders = [('User-agent', header)]
        self.validateHostName(dasHost)
        self.validateHostName(popHost)
        self._dasHost=dasHost
        self._popHost=popHost
        
    def validateHostName(self, hostname):
        #pat = re.compile('^http[s]*://[a-zA-Z0-9\-\.]+$')
        if  not Lexicon.hostname(hostname):
            msg = 'Invalid hostname: %s' % hostname
            raise ValueError(msg)

    def validateSiteName(self, sitename):
        #pat = re.compile('^T[0-9][a-zA-Z0-9_]+$')
        if  not Lexicon.wildcardtier(sitename):
            msg = 'Invalid sitename: %s' % sitename
            raise ValueError(msg)
        
    def get_pop_data(self, site, timestart, timestop):
        """Contact PopDB server and retrieve data for given PopDB query"""
        params  = {'sitename':site, 'tstart': timestart, 'tstop': timestop}
        pophost = self._popHost
        path    = '/popdb/victorinterface/accessedBlocksStat/'
        self.validateHostName(pophost)
        self.validateSiteName(site)
        url = pophost + path
        headers = {"Accept": "application/json"}
        encoded_data = urllib.urlencode(params, doseq=True)
        url += '?%s' % encoded_data
        req  = urllib2.Request(url=url, headers=headers)
        fdesc = self.opener.open(req)
        popdata = fdesc.read()
        fdesc.close()
        try:
            self.pop_data=json.loads(popdata)
        except ValueError, err:
            logger.error('Unable to decode JSON from popdb output:')
            logger.error(popdata)
            raise err
        try:
            self.pop_data[site]
        except KeyError:
            logger.warning('WARNING: empty popularity results for %s' % site)
                        
    def get_das_blockreplica_data(self, site):
        dasHost = self._dasHost
        self.validateHostName(dasHost)
        self.validateSiteName(site)
        dasQuery='block site=%s' % site
        myDas = DASInterface(debug=self._debug)
        self.das_data=myDas.get_das_data(dasHost,dasQuery)

    def get_phedex_blockreplica_data(self, site):
        phedexHost = self._dasHost
        self.validateHostName(phedexHost)
        self.validateSiteName(site)
        path='/phedex/datasvc/json/prod/blockreplicas'
        params = {'node':site}
        encoded_data = urllib.urlencode(params, doseq=True)
        url=phedexHost+path
        url += '?%s' % encoded_data
        headers = {"Accept": "application/json"}
        req  = urllib2.Request(url=url, headers=headers)
        fdesc = self.opener.open(req)
        phedexdata = fdesc.read()
        fdesc.close()
        try:
            phedex_data=json.loads(phedexdata)
        except ValueError, err:
            logger.error('Unable to decode JSON from PhEDEx datasvc output:')
            logger.error(phedexdata)
            raise err
        try:
            phedexReplicaList=phedex_data[u'phedex'][u'block']
            if not phedexReplicaList:
                logger.warning('WARNING: no replicas found at %s' % sitename)
                msg='WARNING: no replicas found at %s' % sitename
                raise ValueError(msg)
            #TEMP HACK: REARRANGE PHEDEX DATA TO LOOK LIKE DAS DATA
            dasData=[]
            for block in phedexReplicaList:
                dasRecord={}
                dasRecord['name']=block['name']
                dasRecord['replica']={}
                for val in ('group','custodial','complete'):
                    dasRecord['replica'][val]=block['replica'][0][val]
                dasRecord['replica']['nfiles']=int(block['replica'][0]['files'])
                dasRecord['replica']['size']=int(block['replica'][0]['bytes'])
                dasRecord['replica']['creation_time']=int(float(block['replica'][0]['time_create']))
                dasBlockRecord={'block':dasRecord}
                dasData.append(dasBlockRecord)
            self.das_data={'data':dasData}
                
        except KeyError, err:
            logger.error("missing key in PhEDEx record")
            logger.error(data)
            raise err
        
            logger.warning('WARNING: empty PhEDEx datasvc results for %s' % site)
        

    def combine(self, sitename, timestart, timestop, incomplete=0, debug=0):
        self.validateSiteName(sitename)
        try:
            popsettings = confSettings()
            interface = popsettings.getSetting("victorinterface", "DATASERVICE_INTERFACE")
            logger.info("using interface: %s - host: %s" % (interface, self._dasHost))
            #self.get_das_blockreplica_data(sitename)
            #COMMENT ABOVE AND UNCOMMENT BELOW TO SWITCH TO PHEDEX
            if (interface == 'phedex'):
                try:
                    self.get_phedex_blockreplica_data(sitename)
                except Exception, err:
                    logger.error("Unable to fetch replica information from PhEDEx")
                    logger.error(err)
                    raise err
            elif (interface == 'das'):
                try:
                    self.get_das_blockreplica_data(sitename)
                except Exception, err:
                    logger.error("Unable to fetch replica information from DAS")
                    logger.error(err)
                    raise err
            else:
                logger.error("Unable to fetch replica information - Unknow module specified in config file: %s" % interface)
                raise Exception("Unable to fetch replica information")
        except PopularityConfigException, err:
            logger.error(err)
            raise err

        try:
            self.get_pop_data(sitename,timestart,timestop)
        except Exception, err:
            logger.error("Unable to fetch popularity information from PopDB")
            logger.error(err)
            raise err

        try:
            data = self.das_data['data']
        except KeyError, err:
            logger.warning("No data in DAS query result")
            raise err

        if not data:
            logger.warning('WARNING: no replicas found at %s' % sitename)
            msg='WARNING: no replicas found at %s' % sitename
            raise ValueError(msg)

        popdict=self.pop_data

        outcoll={}
        
        for row in data:
            if not incomplete and row['block']['replica']['complete'] == 'n':
                continue
            outrep={}
            for val in ('group','custodial','creation_time','nfiles','size'):
                outrep[val]=row['block']['replica'][val]
            try:
                outrep['popularitynacc']=popdict[sitename][row['block']['name']]['NACC']
                outrep['popularitycpu']=popdict[sitename][row['block']['name']]['TOTCPU']

                logger.debug(row['block']['name']+" POPULAR")
                del popdict[sitename][row['block']['name']]
            except KeyError:
                outrep['popularitynacc']=0
                outrep['popularitycpu']=0
                logger.debug(row['block']['name']+" UNPOPULAR")
            outcoll[row['block']['name']]=outrep
        if len(popdict) != 0:
            for row in popdict[sitename]:
                logger.debug(row+" NOTINPHEDEX")
        outdict={sitename:outcoll,'popularitytstart':timestart,'popularitytstop':timestop}
        return outdict

