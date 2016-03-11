from __future__ import absolute_import
from django.conf.urls import *
from . import views as views
from Apps.popCommon.database import popCommonDB
from Apps.popCommon.utils.confSettings import confSettings

#global DBUSER
#DBUSER = 'CMS_EOS_POPULARITY_SYSTEM'
popsettings = confSettings()
DBUSER = popsettings.getSetting("xrdPopularity", "DBUSER")
#sitelist = popCommonDB.getSitesList(DBUSER)


urlpatterns = patterns('',

                       url(r'^$', views.xrdRenderTemplate, {'tmplPath': 'xrdPopularity/xrdDataTierTable.html'}, "xrdIndex"),

                       url(r'^version_log$', views.xrdRenderTemplate, {'tmplPath': 'xrdPopularity/version_log.html'}, "xrdpopularityversionlog"),
                       url(r'^tablesDoc$', views.tablesDoc),

                       ####################
                       ## XRD Monitoring
                       ###################

                       ####################
                       ## XRD Monitoring Table
                       ###################

                       
                       # this renders tables
                       url(r'^xrdmontable$', views.xrdRenderTemplate, {'tmplPath': 'xrdPopularity/xrdMonitoringTable.html'}, "xrdMonTable"),
                       
                       ## this will bprovide the josn (probably will not use)
                       #url(r'^xrdmoninsertionsMI$', views.xrdMonitoring, {'table':'MV_xrdmon_inserts_x_MI'      }, "xrdmoninsertionsMI"),
                       #url(r'^xrdmoninsertions$'  , views.xrdMonitoring, {'table':'MV_xrdmon_inserts_x_H'       }, "xrdmoninsertions"  ),
                       #url(r'^xrdmonstarttime$'   , views.xrdMonitoring, {'table':'MV_xrdmon_starttime_x_H'     }, "xrdmonstarttime"   ),
                       url(r'^xrdmonendtime$', views.xrdMonitoring, {'table':'MV_xrdmon_endtime_x_H'       }, "xrdmonendtime"     ),
                       #url(r'^xrdmonppssrm$'      , views.xrdMonitoring, {'table':'MV_xrdmon_pps_srmmon_test_x_H'}, "xrdmonppssrm"      ),
                       #url(r'^xrdmonppsdteam$'    , views.xrdMonitoring, {'table':'MV_xrdmon_pps_dteam_test_x_H'}, "xrdmonppsdteam"    ),

                       ####################
                       ## XRD Monitoring Plot
                       ###################


                       # this renders plots for xrd monitoring purpose
                       #url(r'^xrdMonitoringPlot$', views.xrdRenderTemplate, {'tmplPath': 'xrdPopularity/xrdMonitoringPlot.html'}, "xrdMonPlot"),
                       url(r'^xrdmonplotaccessrate$', views.xrdRenderTemplate, {'tmplPath': 'xrdPopularity/xrdMonitoringPlotAccessRates.html'}, "xrdMonPlotAccessRate"),
                       url(r'^xrdmonplotppstest$', views.xrdRenderTemplate, {'tmplPath': 'xrdPopularity/xrdMonitoringPlotPPS.html'}, "xrdMonPlotPPS"),
                       
                      
                       # Core: generic url to return in json format pairs [xval, yval] to plot data 
                       url(r'^xrdmonplotdata$', views.xrdMonitoringPlotData, {}, "xrdMonPlotData"),


                       ####################
                       ## XRD Popularity Table
                       ###################
                       

                       ## this renders tables

                       url(r'^xrddatasettable$', views.xrdRenderTemplate, {'tmplPath': 'xrdPopularity/xrdDataSetTable.html'    }, "xrdDataSetTable"    ),
                       url(r'^xrddatatiertable$', views.xrdRenderTemplate, {'tmplPath': 'xrdPopularity/xrdDataTierTable.html'   }, "xrdDataTierTable"   ),
                       url(r'^xrddatasetnametable$', views.xrdRenderTemplate, {'tmplPath': 'xrdPopularity/xrdDataSetNameTable.html'}, "xrdDataSetNameTable"),
                       url(r'^xrduserdatatable$', views.xrdRenderTemplate, {'tmplPath': 'xrdPopularity/xrdUserDataTable.html'    }, "xrdUserDataTable"    ),


                       url(r'^DSStatInTimeWindow$', views.getDSStatInTimeWindow, {'MView':'DS'      }, "xrdDSStatInTimeWindow"      ),
                       url(r'^DataTierStatInTimeWindow$', views.getDSStatInTimeWindow, {'MView':'DataTier'}, "xrdDataTierStatInTimeWindow"),
                       url(r'^DSNameStatInTimeWindow$', views.getDSStatInTimeWindow, {'MView':'DSName'  }, "xrdDSNameStatInTimeWindow"  ),
                       url(r'^UserDSStatInTimeWindow$', views.getDSStatInTimeWindow, {'MView':'UserDS'  }, "xrdUserDSStatInTimeWindow"  ),

                       url(r'^xrduserstattable$', views.xrdRenderTemplate, {'tmplPath': 'xrdPopularity/xrdUserStatTable.html', 'contextRequests': {'datatiers': map(lambda x: x["COLLNAME"], popCommonDB.getDataTierList(DBUSER))} }, "xrdUserStatTable"),
                       url(r'^xrduserstat$', views.getUserStat, {}, "xrdUserStat"),

                       url(r'^xrdlocalglobaluserstattable$', views.xrdRenderTemplate, {'tmplPath': 'xrdPopularity/xrdLocalGlobalUserStatTable.html'}, "xrdLocalGlobalUserStatTable"),
                       url(r'^xrdlocalglobaluserstat$', views.getLocalGlobalUserStat, {}, "xrdLocalGlobalUserStat"),


                       ####################
                       ## XRD Popularity Plot
                       ###################

                       
                                              
                       # this renders plots for xrd popularity ds
                       #FIXME probably remove
                       #url(r'^xrdplotmostpopulardatatier$', views.xrdRenderTemplate, {'tmplPath': 'xrdPopularity/xrdMostPopularSomething.html'}, "xrdPlotMostPopularDataTier"),
                       
                       #
                       ## this renders tables

                       url(r'^xrddatasetplot$', views.xrdRenderTemplate, {'tmplPath': 'xrdPopularity/xrdDataSetPlot.html'    }, "xrdDataSetPlot"    ),
                       url(r'^xrddatatierplot$', views.xrdRenderTemplate, {'tmplPath': 'xrdPopularity/xrdDataTierPlot.html'   }, "xrdDataTierPlot"   ),
                       url(r'^xrddatasetnameplot$', views.xrdRenderTemplate, {'tmplPath': 'xrdPopularity/xrdDataSetNamePlot.html'}, "xrdDataSetNamePlot"),
                       url(r'^xrduserdataplot$', views.xrdRenderTemplate, {'tmplPath': 'xrdPopularity/xrdUserDataPlot.html'   }, "xrdUserDataPlot"   ),
                       url(r'^customDSPlot$', views.xrdRenderTemplate, {'tmplPath': 'xrdPopularity/xrdCustomDataSetPlot.html'}, "xrdCustomdsplot"    ),
                       url(r'^customProcessedDSPlot$', views.xrdRenderTemplate, {'tmplPath': 'xrdPopularity/xrdCustomProcessedDataSetPlot.html'}, "xrdCustomprocesseddsplot"    ),

                       url(r'^getDSdata', views.getTimeEvolutionPlotData, {'MView':'DS'      }, "xrdGetDSPlotData"      ),
                       url(r'^getDTdata', views.getTimeEvolutionPlotData, {'MView':'DataTier'}, "xrdGetDTPlotData"      ),
                       url(r'^getDSNdata', views.getTimeEvolutionPlotData, {'MView':'DSName'  }, "xrdGetDSNPlotData"     ),
                       url(r'^getUserDSdata', views.getTimeEvolutionPlotData, {'MView':'UserDS'  }, "xrdGetUserDSPlotData"  ),
                       url(r'^getSingleDSstat', views.getDataSetStat, {}, "xrdGetSingleDSPlotStat"),
                       url(r'^getSingleProcessedDSstat', views.getProcessedDataSetStat, {}, "xrdGetSingleProcessedDSPlotStat"),


                       #url(r'^getDSstat'  , views.getDSstat               , {                  }, "xrdGetDSstat"      ),

                       # Other JSON
                       url(r'^availableDataSets', views.dataSets, {}, "xrdDataSets"),
                       url(r'^availableProcessedDataSets', views.processedDataSets, {}, "xrdProcessedDataSets"),
                       )

