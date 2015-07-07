# Create your views here.
from django.views.decorators.cache import cache_page
from django.template import Context, loader

from django.utils import simplejson
from django.db import connection, transaction
from django.http import Http404

from collections import defaultdict
import json
from datetime import datetime, date, timedelta

from Apps.popCommon.database import popCommonDB
from Apps.xrdPopularity.database import popDB

import logging
import time
import calendar
import string

import copy

logger = logging.getLogger(__name__)
#---------------------------------------------------------------------
# DATA COLLECTION VIEWS
#---------------------------------------------------------------------

def getxrdMonitoringInTimeWindowJSON(pars):
    data = popDB.xrdStatInTimeWindow(pars)
    logger.info('got data')
    jdata = json.dumps(data)
    return jdata


def getxrdMonitoringInTimeWindowForMultiplePlotsJSON(parList):
    # logger.info('in getxrdMonitoringInTimeWindowForMultiplePlotsJSON')
    
    allData = {'data' : [], "tstop": parList[0].TStop, "tstart": parList[0].TStart} 
    for pars in parList:
        pars.orderby = 'order by xTime'
        data = popDB.xrdStatInTimeWindow(pars)        
        points = [ (a['MILLISECONDSSINCEEPOCH'], float(a[pars.yval]) ) for a in data['DATA']  ]
        allData['data'].append({'name': pars.name , 'data':points})

    # logger.info(parList)
    # logger.info(allData)
    jdata = json.dumps(allData)
    return jdata


#---------------------------------------------------------------------

def getDSStatInTimeWindowJSON(params):
    data = popDB.DSStatInTimeWindow(params)
    jdata = json.dumps(data)
    return jdata
    
#---------------------------------------------------------------------

def getUserStatInTimeWindowJSON(params):
    translationDict = { 'totcpu' : 'TOTCPU', 'naccess' : 'NACC', 'nusers' : 'NUSERS'}
    try:
        params.orderVar = translationDict[params.orderVar]
    except:
        raise Paramvalidationexception('orderby', 'parameter not specified or not matching the options: %s' % traslationDict.keys())

    data = popDB.UserStatInTimeWindow(params)
    if not hasattr(params, 'LocalVsGlobal'):
        data['COLLNAME'] = params.collName
    data['TSTART'] = params.TStart
    data['TSTOP'] = params.TStop
    jdata = simplejson.dumps(data)
    return jdata


#---------------------------------------------------------------------

def getMostPopStatDict(pars):
    data = []
    dataP = popDB.DSStatInTimeWindow(pars) 
    logger.info(dataP)
    params = copy.deepcopy(pars)
    for entry in dataP['DATA'][:params.FirstN]:
        params.collName = entry['COLLNAME']
        #collData = {"COLLNAME" : params.collName}
        #collData.update(popDB.MostPopDSStat(params))
        collData = popDB.MostPopDSStat(params)
        data.append(collData)

    # logger.info('getMostPopStatDict data %s' % data)
    return data




def getTimeEvolutionPlotDataJSON(params):

    translationDict = { 'totcpu' : 'TOTCPU', 'naccess' : 'NACC', 'nusers' : 'NUSERS'}
    try:
        params.orderVar = translationDict[params.orderVar]
    except:
        raise Paramvalidationexception('orderby', 'parameter not specified or not matching the options: %s' % traslationDict.keys())
      

    data = getMostPopStatDict(params)
    res = {'tstart': params.TStart, 'tstop': params.TStop, 'aggr': params.AggrFlag, 'data': data}
    #logger.info('getTimeEvolutionPlotDataJSON data %s' % res)
    
    return json.dumps(res)



#---------------------------------------------------------------------


def getSingleElementStat(par, MView):

    par.table = MView
    data = popDB.MostPopDSStat(par)
    logger.info(par)
    jsonRes = {}
    listRes = []
    series1 = []
    """
    for entry in data['data']:
        millisecondSinceEpoch=1000*calendar.timegm(time.strptime(entry['TDAY'],'%Y/%m/%d'))
        if (par.orderVar == "totcpu"):
            series1.append( [  millisecondSinceEpoch, entry['TOTCPU'] ] )
        elif (par.orderVar == "naccess"):
            series1.append( [  millisecondSinceEpoch, entry['NACC'  ] ] )
        elif (par.orderVar == "nusers"):
            series1.append( [  millisecondSinceEpoch, entry['NUSERS'  ] ] )
    """
    #listRes.append({'name' : data['COLLNAME'], 'data' : series1})
    #jsonRes = {'tstart': par.TStart, 'tstop': par.TStop, 'aggr': par.AggrFlag, 'data': listRes}
    jsonRes = {'tstart': par.TStart, 'tstop': par.TStop, 'aggr': par.AggrFlag, 'data': [data]}

    jdata = json.dumps(jsonRes)
    return jdata

