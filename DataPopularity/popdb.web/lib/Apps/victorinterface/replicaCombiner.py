import logging
import json
import urllib
import platform
import datetime

from Apps.popCommon.utils import Lexicon
from Apps.popCommon.utils.confSettings import confSettings
from Apps.popCommon.PopularityException import PopularityConfigException
from Apps.victorinterface.utils.serviceInterface import popularityDBInterface
#from Apps.victorinterface.utils.serviceInterface import dasInterface

logger = logging.getLogger(__name__)

class replicaCombiner:

    def __init__(self, lastAcc=False):
        self.lastAccOpt = lastAcc
        popsettings = confSettings()
        self.interface = popsettings.getSetting("victorinterface", "DATASERVICE_INTERFACE") + 'Interface'
        try:
            module = __import__('Apps.victorinterface.utils.serviceInterface', globals(), locals(), [self.interface], -1)
            self.replicaInterface = getattr(module, self.interface)
        except Exception as err:
            msg = 'unable to import replica interface: %s ' % self.interface
            logger.error(msg)
            raise Exception(msg)
        self.replicaHost = popsettings.getSetting("victorinterface", "DATASERVICE_HOST")


    def combineNACC(self, params, incomplete = 0):

        sitename = params.SiteName
        source = params.source
        timestart = params.TStart
        timestop = params.TStop

        logger.info("using replica interface: %s - host: %s" % (self.replicaInterface.__name__, self.replicaHost))

        try:
            replica = self.replicaInterface(self.replicaHost)
            replica_data = replica.get_json_data(sitename)
        except Exception as err:
            logger.error("Unable to fetch replica information from %s" % self.replicaInterface.__name__)
            logger.error(err)
            raise err

        try:
            popinterface = popularityDBInterface()
            pop_data = popinterface.get_json_data(sitename, source, timestart, timestop)
        except Exception as err:
            logger.error("Unable to fetch popularity information from PopDB")
            logger.error(err)
            raise err

        try:
            data = replica_data['data']
        except KeyError as err:
            logger.warning("No replica data result")
            raise err

        if not data:
            logger.warning('WARNING: no replicas found at %s' % sitename)
            msg='WARNING: no replicas found at %s' % sitename
            raise ValueError(msg)

        popdict = pop_data

        outcoll = {}

        for row in data:
            if not incomplete and row['block'][0]['replica']['complete'] == 'n':
                continue
            outrep={}

            for val in ('group', 'custodial', 'creation_time', 'nfiles', 'size'):
                if (val == 'group') and (row['block'][0]['replica'][val] == ''):
                    outrep[val] = None
                else:
                    outrep[val]=row['block'][0]['replica'][val]
            try:
                outrep['popularitynacc']=popdict[sitename][row['block'][0]['name']]['NACC']
                outrep['popularitycpu']=popdict[sitename][row['block'][0]['name']]['TOTCPU']

                logger.debug(row['block'][0]['name']+" POPULAR")
                del popdict[sitename][row['block'][0]['name']]
            except KeyError:
                outrep['popularitynacc']=0
                outrep['popularitycpu']=0
                logger.debug(row['block'][0]['name']+" UNPOPULAR")
            outcoll[row['block'][0]['name']]=outrep
        if len(popdict) != 0:
            for row in popdict[sitename]:
                logger.debug(row+" NOTINPHEDEX")
        outdict = {sitename:outcoll,'popularitytstart':timestart,'popularitytstop':timestop}
        return outdict

    def combineLastAcc(self, params, incomplete = 0):

        sitename = params.SiteName
        source = params.source
        #timestart = params.TStart
        #timestop = params.TStop

        logger.info("using replica interface: %s - host: %s" % (self.replicaInterface.__name__, self.replicaHost))

        try:
            replica = self.replicaInterface(self.replicaHost)
            replica_data = replica.get_json_data(sitename)
        except Exception as err:
            logger.error("Unable to fetch replica information from %s" % self.replicaInterface.__name__)
            logger.error(err)
            raise err

        try:
            popinterface = popularityDBInterface(lastAcc = True)
            pop_data = popinterface.get_json_data(sitename, source)
        except Exception as err:
            logger.error("Unable to fetch popularity information from PopDB")
            logger.error(err)
            raise err

        try:
            data = replica_data['data']
        except KeyError as err:
            logger.warning("No replica data result")
            raise err

        if not data:
            logger.warning('WARNING: no replicas found at %s' % sitename)
            msg='WARNING: no replicas found at %s' % sitename
            raise ValueError(msg)

        popdict = pop_data
        outcoll = {}

        for row in data:
            if not incomplete and row['block'][0]['replica']['complete'] == 'n':
                continue
            outrep={}

            for val in ('group', 'custodial', 'creation_time', 'nfiles', 'size'):
                if (val == 'group') and (row['block'][0]['replica'][val] == ''):
                    outrep[val] = None
                else:
                    outrep[val]=row['block'][0]['replica'][val]
            try:
                outrep['lastdayacc'  ] = popdict[sitename][row['block'][0]['name']][popdict[sitename][row['block'][0]['name']].keys()[0]]
                logger.debug(row['block'][0]['name']+" POPULAR")
                del popdict[sitename][row['block'][0]['name']]

            except KeyError:
                outrep['lastdayacc'] = -1
                logger.debug(row['block'][0]['name']+" UNPOPULAR")

            outcoll[row['block'][0]['name']]=outrep
        if len(popdict) != 0:
            for row in popdict[sitename]:
                logger.debug(row+" NOTINPHEDEX")
        outdict = {sitename:outcoll}
        return outdict


    def combine(self, params, incomplete = 0):

        if self.lastAccOpt:
            return self.combineLastAcc(params, incomplete)
        else:
            return self.combineNACC(params, incomplete)


