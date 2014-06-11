from django.http import HttpResponse, HttpResponseServerError, HttpResponseBadRequest
import json
import time
from datetime import datetime, date, timedelta

from Apps.victorinterface.database import victorinterfaceDB
from Apps.victorinterface.utils.Victorinterfaceparams import victorinterfaceparams
from Apps.victorinterface.replicaPopularity import replicaPopularity
from Apps.popCommon.PopularityException import Paramvalidationexception
from Apps.victorinterface.replicaCombiner import replicaCombiner

import logging

logger = logging.getLogger(__name__)


def getCollectionInSiteWithStat(request, collType, lastAcc=False, source=''):
    stop = datetime.now()
    start = datetime.now() - timedelta(days=30)
    par = victorinterfaceparams()
    try:
        par.setSiteName(request.GET.get('sitename', 'T%'))
        logger.info('debug. siteName = %s' % par.SiteName)
    
        source = request.GET.get('source', '')
        if source=='':
            if par.SiteName == 'T2_CH_CERN' or par.SiteName == 'T0_CH_CERN':
                source = 'xrootd'
                par.SiteName = 'T2_CH_CERN'
            else:
                source = 'crab'
        par.setSource(source)


        if lastAcc:
            data = victorinterfaceDB.WhatInSiteWithStatLastAcc(collType, par)
        else:
            par.setTStart(request.GET.get('tstart', start.strftime("%Y-%m-%d")))
            par.setTStop(request.GET.get('tstop', stop.strftime("%Y-%m-%d")))
            data = victorinterfaceDB.WhatInSiteWithStat(collType, par)
    except Paramvalidationexception as e:
        #return HttpResponseBadRequest("Given %s not valid (%s)" % (e.param, e.cause))
        return HttpResponseBadRequest(e.getmessage())
    except victorinterfaceDB.PopularityDBException as dbe:
        #return HttpResponseBadRequest("Given %s not valid (%s)" % (e.param, e.cause))
        return HttpResponseServerError(dbe.getmessage())
    except Exception as ex:
        return HttpResponseServerError(ex)

    return HttpResponse(json.dumps(data))


def getCombinedDASPopInfo(request, lastAcc=False):
    stop = datetime.now()
    start = datetime.now() - timedelta(days=30)
    par = victorinterfaceparams()

    try:
        par.setSiteName(request.GET.get('sitename', 'T%'))
        logger.info('debug. siteName = %s' % par.SiteName)
        #data = replicaPopularity(par)

        source = request.GET.get('source', '')
        if source=='':
            if par.SiteName == 'T2_CH_CERN' or par.SiteName == 'T0_CH_CERN':
                source = 'xrootd'
                par.SiteName = 'T2_CH_CERN'
            else:
                source = 'crab'
        par.setSource(source)

        if lastAcc:
            combiner = replicaCombiner(lastAcc = True)
        else:
            par.setTStart(request.GET.get('tstart', start.strftime("%Y-%m-%d")))
            par.setTStop(request.GET.get('tstop', stop.strftime("%Y-%m-%d")))
            combiner = replicaCombiner()
        data = combiner.combine(par)

    except Paramvalidationexception as e:
        #return HttpResponseBadRequest("Given %s not valid (%s)" % (e.param, e.cause))
        return HttpResponseBadRequest(e.getmessage())
    except Exception as ex:
        return HttpResponseServerError(ex)

    return HttpResponse(json.dumps(data))

