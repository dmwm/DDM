from django.template import loader, RequestContext
from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.views.decorators.cache import cache_page
import json

from Apps.popCommon.database import popCommonDB
from Apps.popCommon.utils import utility
from Apps.xrdPopularity.utils.PopularityParams import Popularityparams, Userstatparams, Paramvalidationexception
from Apps.xrdPopularity.database import popDB
from Apps.xrdPopularity.views import data_collection as dataH 

import logging
import time
import calendar
import string
from datetime import datetime, date, timedelta
from copy import deepcopy

logger = logging.getLogger(__name__)

DBUSER = 'CMS_EOS_POPULARITY_SYSTEM'
#----------------------------------------------------------
# RENDERING VIEWS
#----------------------------------------------------------

# This is a generic method to render an html template 
def xrdRenderTemplate(request, tmplPath='', contextRequests = {}):
    tmpl = loader.get_template(tmplPath)
    cont = RequestContext(request, contextRequests)
    return HttpResponse(tmpl.render(cont))

#---------------------------------------------------------------------

def tablesDoc(request):
    tmpl = loader.get_template("xrdPopularity/docexample.html")
    cont = RequestContext(request)
    return HttpResponse(tmpl.render(cont))    

#---------------------------------------------------------------------

def xrdMonitoring(request,table=''):
    logger.info("collecting data for view xrdMonitoring %s" % (table) )
    stop = datetime.now()
    start = datetime.now() - timedelta(days = 7)
    pars = Popularityparams()

    try:
        pars.setTStart(request.GET.get('tstart', start.strftime("%Y-%m-%d")))
        pars.setTStop(request.GET.get('tstop', stop.strftime("%Y-%m-%d")))
        pars.table = table
        
        jdata = dataH.getxrdMonitoringInTimeWindowJSON(pars)
            
    except Paramvalidationexception as e:           
        return HttpResponseBadRequest(e.getmessage())
    except popDB.PopularityDBException as dbe:
        return HttpResponseServerError(dbe.getmessage())
    except Exception as ex:
        return HttpResponseServerError(ex) 
    
    return HttpResponse(jdata)

    
def xrdMonitoringPlotData(request):
    logger.info("collecting data for view xrdMonitoringPlotData " )


    plotOptions = {
        'inserttime_x_MI' : 'MV_xrdmon_inserts_x_MI'      
        ,'inserttime_x_H' : 'MV_xrdmon_inserts_x_H'       
        ,'starttime_x_H' : 'MV_xrdmon_starttime_x_H'     
        ,'starttime_norepl_x_H' : 'MV_xrdmon_starttime_norepl_x_H'
        ,'starttime_repl_x_H' : 'MV_xrdmon_starttime_repl_x_H'             
        ,'endtime_x_H' : 'MV_xrdmon_endtime_x_H'       
        ,'pps_srmmon_x_H' : 'MV_xrdmon_pps_srmmon_test_x_H'
        ,'pps_dteam_x_H' : 'MV_xrdmon_pps_dteam_test_x_H'
        ,'avg_traffic_x_H_norepl' : 'MV_xrdmon_procTime_x_H_aggr1'
        ,'avg_traffic_x_H_repl' : 'MV_xrdmon_procTime_x_H_aggr2'
        }

    yValueOptions = {
        'absolute' : 'YVALUE'
        ,'rate'    : 'RATE'
        ,'totgb'   : 'TOTGB'
        ,'traffic' : 'MEANTRAFFICINMBS'
        ,'totproctime' : 'TOTPROCTIMEINSEC'
        ,'meanproctime' : 'MEANPROCTIMEINH'
        }
    
    stop = datetime.now()
    start = datetime.now() - timedelta(days = 7)
    pars = Popularityparams()

    try:
        queryDict = request.GET

        pars.setTStart(queryDict.get('tstart', start.strftime("%Y-%m-%d")))
        pars.setTStop (queryDict.get('tstop',  stop.strftime("%Y-%m-%d")))

        plList = queryDict.getlist('plot')
        yvList = queryDict.getlist('yval')

        try:
            tableList = [ plotOptions[pl] for pl in plList ]
        except:
            raise Paramvalidationexception('plot', 'option not specified or not matching the options: plot=%s' % yValueOptions.keys())

        try:    
            if  len(tableList) != len(yvList): 
                # in case the len of the two list is different, use just the first value pf yvalList
                yvalList = [ yValueOptions[yvList[0]] for x in plList ] 
            else:
                yvalList = [ yValueOptions[yv]        for yv in yvList ]
        except:
            raise Paramvalidationexception('plot', 'option not specified: yval=%s' % yValueOptions.keys())
        
        parList = []
        for pl, table, yval in zip(plList, tableList, yvalList):    
            pars.name  = pl
            pars.table = table
            pars.yval  = yval
            parList.append(deepcopy(pars))

        jdata = dataH.getxrdMonitoringInTimeWindowForMultiplePlotsJSON(parList)

        return HttpResponse(jdata)

    except Paramvalidationexception as e:           
        return HttpResponseBadRequest(e.getmessage())
    except popDB.PopularityDBException as dbe:
        return HttpResponseServerError(dbe.getmessage())
    except Exception as ex:
        return HttpResponseServerError(ex) 
    

#--------------------------------------------------------------------

def dataSets(request):
    data = popCommonDB.getDataSetList(DBUSER)
    jdata = {'DATA': data}
    jsondata = json.dumps(jdata)
    return HttpResponse(jsondata)

def processedDataSets(request):
    data = popCommonDB.getProcessedDataSetList(DBUSER)
    jdata = {'DATA': data}
    jsondata = json.dumps(jdata)
    return HttpResponse(jsondata)        

#---------------------------------------------------------------------

def getDSStatInTimeWindow(request,MView=''):
    stop = datetime.now()
    start = datetime.now() - timedelta(days = 7)
    par = Popularityparams()

    par.table = MView
    try:
        par.setTStart(request.GET.get('tstart', start.strftime("%Y-%m-%d")))
        par.setTStop(request.GET.get('tstop', stop.strftime("%Y-%m-%d")))
        
        par.setOrder(request.GET.get('orderby', 'totcpu'))

        par.setIsCentralUser(request.GET.get('centraluser', '0'))
        jdata = dataH.getDSStatInTimeWindowJSON(par)
        
    except Paramvalidationexception as e:
        return HttpResponseBadRequest(e.getmessage())
    except popDB.PopularityDBException as dbe:
        return HttpResponseServerError(dbe.getmessage())
    except Exception as ex:
        return HttpResponseServerError(ex)
        
    return HttpResponse(jdata)


#---------------------------------------------------------------------

@cache_page(60 * 60)
def getUserStat(request):

    DBUSER = 'CMS_EOS_POPULARITY_SYSTEM'

    stop = datetime.now() - timedelta(days=1)
    start = stop - timedelta(days=7)

    par = Userstatparams()
    try:
        par.setTStart(request.GET.get('tstart', start.strftime("%Y-%m-%d")))
        par.setTStop(request.GET.get('tstop', stop.strftime("%Y-%m-%d")))
        par.setCollName(request.GET.get('collname', 'AOD'))
        # par.CollName = 'RECO'
        par.setOrder(request.GET.get('orderby', 'totcpu'))
        jdata = dataH.getUserStatInTimeWindowJSON(par)

    #except Exception, e:
    #    raise e
    except Paramvalidationexception as e:
        return HttpResponseBadRequest(e.getmessage())
    except popDB.PopularityDBException as dbe:
        return HttpResponseServerError(dbe.getmessage())
    except Exception as ex:
        return HttpResponseServerError(ex)

    return HttpResponse(jdata)

#---------------------------------------------------------------------

def getLocalGlobalUserStat(request):
    stop = datetime.now() - timedelta(days=1)
    start = stop - timedelta(days=7)

    par = Userstatparams()
    try:
        par.setTStart(request.GET.get('tstart', start.strftime("%Y-%m-%d")))
        par.setTStop(request.GET.get('tstop', stop.strftime("%Y-%m-%d")))
        par.setOrder(request.GET.get('orderby', 'totcpu'))
        par.LocalVsGlobal = True
        jdata = dataH.getUserStatInTimeWindowJSON(par)

    except Paramvalidationexception as e:
        return HttpResponseBadRequest(e.getmessage())
    except popDB.PopularityDBException as dbe:
        return HttpResponseServerError(dbe.getmessage())
    except Exception as ex:
        return HttpResponseServerError(ex)

    return HttpResponse(jdata)

#---------------------------------------------------------------------

def getTimeEvolutionPlotData(request,MView=''):

    stop = datetime.now()
    start = datetime.now() - timedelta(days=7)
    par = Popularityparams()

    par.table = MView
    try:
        par.setTStart(request.GET.get('tstart', start.strftime("%Y-%m-%d")))
        par.setTStop(request.GET.get('tstop', stop.strftime("%Y-%m-%d")))
        par.setAggregation(request.GET.get('aggr', 'day'))
        par.setN(request.GET.get('n', '1'))

        par.setIsCentralUser(request.GET.get('centraluser', '0'))
        
        par.setOrder(request.GET.get('orderby', 'totcpu'))
        par.setSiteName(request.GET.get('sitename', 'summary'))
        if (par.FirstN == 0):
            return HttpResponseBadRequest("Given n not valid (param must be > 0)")


        jdata = dataH.getTimeEvolutionPlotDataJSON(par)
        return HttpResponse(jdata)
    
    except Paramvalidationexception as e:
        return HttpResponseBadRequest(e.getmessage())
    except popDB.PopularityDBException as dbe:
        return HttpResponseServerError(dbe.getmessage())
    except Exception as ex:
        return HttpResponseServerError(ex)

#----------------------------------------------------------------------------------------

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
        par.setIsCentralUser(request.GET.get('centraluser', '0'))
        par.setOrder(request.GET.get('orderby', 'totcpu'))
        par.setSiteName(request.GET.get('sitename', 'summary'))

        #par.table = 'DS'
        """ 
        data indexing start from 0
        """
        data = dataH.getSingleElementStat(par, 'DS')

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
        par.setIsCentralUser(request.GET.get('centraluser', '0'))
        par.setOrder(request.GET.get('orderby', 'totcpu'))
        par.setSiteName(request.GET.get('sitename', 'summary'))

        #par.table = 'DS'
        """ 
        data indexing start from 0
        """
        data = dataH.getSingleElementStat(par, 'DSName')

    except Paramvalidationexception as e:
        #return HttpResponseBadRequest("Given %s not valid (%s)" % (pEx.param, pEx.cause))
        return HttpResponseBadRequest(e.getmessage())
    except popDB.PopularityDBException as dbe:
        #return HttpResponseBadRequest("Given %s not valid (%s)" % (e.param, e.cause))
        return HttpResponseServerError(dbe.getmessage())
    except Exception as ex:
        return HttpResponseServerError(ex)

    return HttpResponse(data)
