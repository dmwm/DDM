# Create your views here.
from django.views.decorators.cache import cache_page
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.utils import simplejson
from django.db import connection, transaction
from django.http import Http404

from collections import defaultdict
import json
from datetime import datetime, date, timedelta

from Apps.popCommon.utils import utility
#from Apps.popCommon.utils import paramsValidation
#from Apps.popCommon.utils.paramsValidation import ParamValidationException
from Apps.popularity.utils.PopularityParams import Popularityparams, Userstatparams, Paramvalidationexception
from Apps.popCommon.database import popCommonDB
from Apps.popularity.database import popDB
from Apps.popCommon.utils.confSettings import confSettings

import logging
import time
import calendar
import string


logger = logging.getLogger(__name__)

popsettings = confSettings()
DBUSER = popsettings.getSetting("popularity", "DBUSER")


#---------------------------------------------------------------------
# DATA COLLECTION VIEWS
#---------------------------------------------------------------------

@cache_page(60*60)
def dataSets(request):
    data = popCommonDB.getDataSetList(DBUSER)
    jdata = {'DATA': data}
    jsondata = json.dumps(jdata)
    return HttpResponse(jsondata)

@cache_page(60*60)
def dataTiers(request):
    data = popCommonDB.getDataTierList(DBUSER)
    jdata = {'DATA': data}
    jsondata = json.dumps(jdata)
    return HttpResponse(jsondata)

@cache_page(60*60)
def processedDataSets(request):
    data = popCommonDB.getProcessedDataSetList(DBUSER)
    jdata = {'DATA': data}
    jsondata = json.dumps(jdata)
    return HttpResponse(jsondata)

#---------------------------------------------------------------------

def _getDSStatInTimeWindowJSON(params,MView=''):
    data = popDB.DSStatInTimeWindow(params, MView)
    data['SITENAME']=params.SiteName
    jdata = json.dumps(data)
    return jdata

def getDSStatInTimeWindow(request,MView=''):
    stop = datetime.now()
    start = datetime.now() - timedelta(days = 7)
    par = Popularityparams()
    try:
        par.setTStart(request.GET.get('tstart', start.strftime("%Y-%m-%d")))
        par.setTStop(request.GET.get('tstop', stop.strftime("%Y-%m-%d")))

        par.setOrder(request.GET.get('orderby', 'totcpu'))
        par.setSiteName(request.GET.get('sitename', 'summary'))
        jdata = _getDSStatInTimeWindowJSON(par, MView)

    except Paramvalidationexception as e:           
        #return HttpResponseBadRequest("Given %s not valid (%s)" % (e.param, e.cause))
        return HttpResponseBadRequest(e.getmessage())
    except popDB.PopularityDBException as dbe:
        #return HttpResponseBadRequest("Given %s not valid (%s)" % (e.param, e.cause))
        return HttpResponseServerError(dbe.getmessage())
    except Exception as ex:
        return HttpResponseServerError(ex) 
    

    #jdata = _getDSStatInTimeWindowJSON(par,MView)
    return HttpResponse(jdata)

#---------------------------------------------------------------------

def _getMostPopStatDict(params,MView=''):
    data = {}
    dataP = popDB.DSStatInTimeWindow(params, MView) 
    i = 0
    for entry in dataP['DATA']:
        collName = entry['COLLNAME']
        collData = {"COLLNAME" : collName}
        collData.update(popDB.MostPopDSStat(params, MView, collName))
        data[i]=collData.copy()
        i+=1
        if i >= params.FirstN and params.FirstN>0:
            break
    return data


#--------------------------------------------------------------------------------

def _getUserStatInTimeWindowJSON(params):
    data = popDB.UserStatInTimeWindow(params)
    data['COLLNAME'] = params.CollName
    data['TSTART'] = params.TStart
    data['TSTOP'] = params.TStop
    jdata = simplejson.dumps(data)
    return jdata

def getUserStat(request):
    stop = datetime.now() - timedelta(days=1)
    start = stop - timedelta(days=7)
    #par = paramsValidation.userStatParams(request)
    par = Userstatparams()
    try:
        par.setTStart(request.GET.get('tstart', start.strftime("%Y-%m-%d")))
        par.setTStop(request.GET.get('tstop', stop.strftime("%Y-%m-%d")))
        par.setCollName(request.GET.get('collname', 'AOD'))
        par.setOrder(request.GET.get('orderby', 'totcpu'))
        jdata = _getUserStatInTimeWindowJSON(par)

    except Paramvalidationexception as e:
        #return HttpResponseBadRequest("Given %s not valid (%s)" % (e.param, e.cause))
        return HttpResponseBadRequest(e.getmessage())
    except popDB.PopularityDBException as dbe:
        #return HttpResponseBadRequest("Given %s not valid (%s)" % (e.param, e.cause))
        return HttpResponseServerError(dbe.getmessage())
    except Exception as ex:
        return HttpResponseServerError(ex)

    #jdata = _getUserStatInTimeWindowJSON(par)
    return HttpResponse(jdata)

#--------------------------------------------------------------------------------


def _getCorruptedFilesInTimeWindowJSON(params):
    data = popDB.CorruptedFilesInTimeWindow(params)
    jdata = simplejson.dumps(data)
    return jdata

def _getCorruptedFilesInTimeWindowJSON(params):
    data = popDB.CorruptedFilesInTimeWindow(params)
    jdata = simplejson.dumps(data)
    return jdata

@cache_page(60*60, cache="onfile")
def getCorruptedFiles(request, dbview):
    par = Popularityparams()
    logger.info(dbview)
    dbviewValidation = {'detail':'v_CorruptedFilesDetail', 'siteSummary': 'v_corruptedFilesSiteSummary', 'dsSummary':'v_corruptedFilesDSSummary'}

    try:
        par.dbview = dbviewValidation[dbview]        
        logger.info(par.dbview)
    except Exception as ex:        
        raise ex
        return HttpResponseServerError(ex)
    
    try:
        par.setSiteName(request.GET.get('sitename', 'summary'))
        jdata = _getCorruptedFilesInTimeWindowJSON(par)
    except Paramvalidationexception as e:
        #return HttpResponseBadRequest("Given %s not valid (%s)" % (pEx.param, pEx.cause))
        return HttpResponseBadRequest(e.getmessage())
    except popDB.PopularityDBException as dbe:
        #return HttpResponseBadRequest("Given %s not valid (%s)" % (e.param, e.cause))
        return HttpResponseServerError(dbe.getmessage())
    except Exception as ex:
        return HttpResponseServerError(ex)


    #jdata = _getCorruptedFilesInTimeWindowJSON(par)
    return HttpResponse(jdata)



#-------------------------------------------------------------------------
"""
DEPRECATED: Not used anymore to get data for plot, replaced by getTimeEvolutionPlotData
"""
def getPlotData(request,MView=''):
    stop = datetime.now()
    start = datetime.now() - timedelta(days=7)
    par = Popularityparams()
    try:
        par.setTStart(request.GET.get('tstart', start.strftime("%Y-%m-%d")))
        par.setTStop(request.GET.get('tstop', stop.strftime("%Y-%m-%d")))
        par.setAggregation(request.GET.get('aggr', 'day'))
        par.setN(request.GET.get('n', '1'))


        par.setOrder(request.GET.get('orderby', 'totcpu'))
        par.setSiteName(request.GET.get('sitename', 'summary'))
        if (par.FirstN == 0):
            return HttpResponseBadRequest("Given n not valid (param must be > 0)")


        """
        data indexing start from 0
        """
        idx = (par.FirstN)-1
        
        data= _getMostPopStatDict(par, MView)        

    except Paramvalidationexception as e:
        return HttpResponseBadRequest(e.getmessage())
    except popDB.PopularityDBException as dbe:
        return HttpResponseServerError(dbe.getmessage())
    except Exception as ex:
        return HttpResponseServerError(ex)


    collData = data[idx]

    series1 = []
    series2 = []

    for entry in collData['DATA']:
        millisecondSinceEpoch=1000*calendar.timegm(time.strptime(entry['TDAY'], '%Y/%m/%d'))
        series1.append( [  millisecondSinceEpoch, entry['TOTCPU'] ] )
        series2.append( [  millisecondSinceEpoch, entry['NACC'  ] ] )  
    
    jsonRes = {'label' : collData['COLLNAME'], 'data' : series1}

    jdata = json.dumps(jsonRes)
    
    return HttpResponse(jdata)

def getTimeEvolutionPlotData(request,MView=''):
    stop = datetime.now()
    start = datetime.now() - timedelta(days=7)
    par = Popularityparams()
    try:
        par.setTStart(request.GET.get('tstart', start.strftime("%Y-%m-%d")))
        par.setTStop(request.GET.get('tstop', stop.strftime("%Y-%m-%d")))
        par.setAggregation(request.GET.get('aggr', 'day'))
        par.setN(request.GET.get('n', '1'))


        par.setOrder(request.GET.get('orderby', 'totcpu'))
        par.setSiteName(request.GET.get('sitename', 'summary'))
        if (par.FirstN == 0):
            return HttpResponseBadRequest("Given n not valid (param must be > 0)")


        """
        data indexing start from 0
        """
        idx = (par.FirstN)-1
        logger.info(MView)
        data = _getMostPopStatDict(par, MView)

    except Paramvalidationexception as e:
        #return HttpResponseBadRequest("Given %s not valid (%s)" % (pEx.param, pEx.cause))
        return HttpResponseBadRequest(e.getmessage())
    except popDB.PopularityDBException as dbe:
        #return HttpResponseBadRequest("Given %s not valid (%s)" % (e.param, e.cause))
        return HttpResponseServerError(dbe.getmessage())
    except Exception as ex:
        return HttpResponseServerError(ex)

    jsonRes = {}
    listRes = []
    for i in data:
        series1 = []
        series2 = []
        for entry in data[i]['DATA']:
            millisecondSinceEpoch=1000*calendar.timegm(time.strptime(entry['TDAY'], '%Y/%m/%d'))
            if (par.orderVar == "totcpu"):
                series1.append( [  millisecondSinceEpoch, entry['TOTCPU'] ] )
            elif (par.orderVar == "naccess"):
                series1.append( [  millisecondSinceEpoch, entry['NACC'  ] ] )
            elif (par.orderVar == "nusers"):
                series1.append( [  millisecondSinceEpoch, entry['NUSERS'  ] ] )

        listRes.append({'name' : data[i]['COLLNAME'], 'data' : series1})
            #,
            #            {'label' : 'NACC', 'yaxis' : 1 , 'data' : series2}
            #             ]

    jsonRes = {'tstart': par.TStart, 'tstop': par.TStop, 'aggr': par.AggrFlag, 'data': listRes}
    jdata = json.dumps(jsonRes)

    return HttpResponse(jdata)

def getDataSetStat(request):
    stop = datetime.now()
    start = datetime.now() - timedelta(days=7)
    par = Popularityparams()
    try:
        par.setTStart(request.GET.get('tstart', start.strftime("%Y-%m-%d")))
        par.setTStop(request.GET.get('tstop', stop.strftime("%Y-%m-%d")))
        par.setAggregation(request.GET.get('aggr', 'day'))
        par.setDataSet(request.GET.get('name'))
        par.setN('1')
        par.setOrder(request.GET.get('orderby', 'totcpu'))
        par.setSiteName(request.GET.get('sitename', 'summary'))
        """ 
        data indexing start from 0
        """
        data = _getSingleElementStat(par, 'DS')

    except Paramvalidationexception as e:
        #return HttpResponseBadRequest("Given %s not valid (%s)" % (pEx.param, pEx.cause))
        return HttpResponseBadRequest(e.getmessage())
    except popDB.PopularityDBException as dbe:
        #return HttpResponseBadRequest("Given %s not valid (%s)" % (e.param, e.cause))
        return HttpResponseServerError(dbe.getmessage())
    except Exception as ex:
        return HttpResponseServerError(ex)

    return HttpResponse(data)

def getDataTierStat(request):
    stop = datetime.now()
    start = datetime.now() - timedelta(days=7)
    par = Popularityparams()
    try:
        par.setTStart(request.GET.get('tstart', start.strftime("%Y-%m-%d")))
        par.setTStop(request.GET.get('tstop', stop.strftime("%Y-%m-%d")))
        par.setAggregation(request.GET.get('aggr', 'day'))
        par.setDataTier(request.GET.get('name'))
        par.setN('1')
        par.setOrder(request.GET.get('orderby', 'totcpu'))
        par.setSiteName(request.GET.get('sitename', 'summary'))
        """ 
        data indexing start from 0
        """
        data = _getSingleElementStat(par, 'DataTier')

    except Paramvalidationexception as e:
        #return HttpResponseBadRequest("Given %s not valid (%s)" % (pEx.param, pEx.cause))
        return HttpResponseBadRequest(e.getmessage())
    except popDB.PopularityDBException as dbe:
        #return HttpResponseBadRequest("Given %s not valid (%s)" % (e.param, e.cause))
        return HttpResponseServerError(dbe.getmessage())
    except Exception as ex:
        return HttpResponseServerError(ex)

    return HttpResponse(data)

def getProcessedDataSetStat(request):
    stop = datetime.now()
    start = datetime.now() - timedelta(days=7)
    par = Popularityparams()
    try:
        par.setTStart(request.GET.get('tstart', start.strftime("%Y-%m-%d")))
        par.setTStop(request.GET.get('tstop', stop.strftime("%Y-%m-%d")))
        par.setAggregation(request.GET.get('aggr', 'day'))
        par.setProcessedDataSet(request.GET.get('name'))
        par.setN('1')
        par.setOrder(request.GET.get('orderby', 'totcpu'))
        par.setSiteName(request.GET.get('sitename', 'summary'))
        """ 
        data indexing start from 0
        """
        data = _getSingleElementStat(par, 'DSName')
        
    except Paramvalidationexception as e:
        #return HttpResponseBadRequest("Given %s not valid (%s)" % (pEx.param, pEx.cause))
        return HttpResponseBadRequest(e.getmessage())
    except popDB.PopularityDBException as dbe:
        #return HttpResponseBadRequest("Given %s not valid (%s)" % (e.param, e.cause))
        return HttpResponseServerError(dbe.getmessage())
    except Exception as ex:
        return HttpResponseServerError(ex)

    return HttpResponse(data)


def _getSingleElementStat(par, MView):
   
    data = popDB.MostPopDSStat(par, MView, par.CollName)

    jsonRes = {}
    listRes = []
    series1 = []
    for entry in data['DATA']:
        millisecondSinceEpoch=1000*calendar.timegm(time.strptime(entry['TDAY'], '%Y/%m/%d'))
        if (par.orderVar == "totcpu"):
            series1.append( [  millisecondSinceEpoch, entry['TOTCPU'] ] )
        elif (par.orderVar == "naccess"):
            series1.append( [  millisecondSinceEpoch, entry['NACC'  ] ] )
        elif (par.orderVar == "nusers"):
            series1.append( [  millisecondSinceEpoch, entry['NUSERS'  ] ] )

    listRes.append({'name' : data['COLLNAME'], 'data' : series1})
    jsonRes = {'tstart': par.TStart, 'tstop': par.TStop, 'aggr': par.AggrFlag, 'data': listRes}

    jdata = json.dumps(jsonRes)
    return jdata

