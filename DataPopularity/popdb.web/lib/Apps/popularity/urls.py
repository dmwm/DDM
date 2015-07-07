from django.conf.urls import *
from Apps.popCommon.database import popCommonDB
from Apps.popCommon.utils.confSettings import confSettings

#from popularity.views import data_views
#from popularity.views import rendering_views
#from Popularity.apps.popularity.views import rendering_views
from Apps.popularity.views import data_collection as getter
from Apps.popularity.views import rendering_views as render



popsettings = confSettings()
DBUSER = popsettings.getSetting("popularity", "DBUSER")
sitelist = popCommonDB.getSitesList(DBUSER)

urlpatterns = patterns('',

                       #url(r'^$', views.index, {}, "popularityindex"),
                       url(r'^$', render.renderTemplate, {'tmplPath': 'popularity/index.html', 'contextRequests': {"siteslist": popCommonDB.getSitesList(DBUSER)}    }, "popularityindex"    ),
                       
                       # Plots
                       url(r'^dataTier$', render.renderTemplate, {'tmplPath': 'popularity/dataTierPlot.html'   , 'contextRequests': {"siteslist": sitelist}    }, "datatierplot"   ),
                       url(r'^dataSetPlot$', render.renderTemplate, {'tmplPath': 'popularity/dataSetPlot.html'    , 'contextRequests': {"siteslist": sitelist}    }, "datasetplot"    ),
                       url(r'^dataSetNamePlot$', render.renderTemplate, {'tmplPath': 'popularity/dataSetNamePlot.html', 'contextRequests': {"siteslist": sitelist}    }, "datasetnameplot"),

                       url(r'^customDSPlot$', render.renderTemplate, {'tmplPath': 'popularity/customDataSetPlot.html'         , 'contextRequests': {"siteslist": sitelist}    }, "customdsplot" ),
                       url(r'^customDTPlot$', render.renderTemplate, {'tmplPath': 'popularity/customDataTierPlot.html'        , 'contextRequests': {"siteslist": sitelist}    }, "customdtplot" ),
                       url(r'^customProcessedDSPlot$', render.renderTemplate, {'tmplPath': 'popularity/customProcessedDataSetPlot.html', 'contextRequests': {"siteslist": sitelist}    }, "customdsnplot"),

                       url(r'^dataTierBar$', render.renderTemplate, {'tmplPath': 'popularity/dataTierBar.html', 'contextRequests': {"siteslist": sitelist}    }, "datatierbarplot"    ),


                       # Tables
                       url(r'^userStat$', render.renderTemplate, {'tmplPath': 'popularity/userStat.html', 'contextRequests': {"datatiers":  map(lambda x: x["COLLNAME"], popCommonDB.getDataTierList(DBUSER))}    }, "userstat"    ),

                       url(r'^corruptedFiles$', render.renderTemplate, {'tmplPath': 'popularity/corruptedFiles.html'               }, "corruptedfiles"             ),
                       url(r'^corruptedFilesSiteSummary$', render.renderTemplate, {'tmplPath': 'popularity/corruptedFilesSiteSummary.html'    }, "corruptedfilesSiteSummary"  ),
                       url(r'^corruptedFilesDSSummary$', render.renderTemplate, {'tmplPath': 'popularity/corruptedFilesDSSummary.html'      }, "corruptedfilesDSSummary"    ),

                       url(r'^dataSetTable$', render.renderTemplate, {'tmplPath': 'popularity/dataSetTable.html'    , 'contextRequests': {"siteslist": sitelist} }, "datasettable"     ),
                       url(r'^dataSetNameTable$', render.renderTemplate, {'tmplPath': 'popularity/dataSetNameTable.html', 'contextRequests': {"siteslist": sitelist} }, "datasetnametable" ),
                       url(r'^dataTierTable$', render.renderTemplate, {'tmplPath': 'popularity/index.html'           , 'contextRequests': {"siteslist": sitelist} }, "datatiertable"    ),

                       # Plots JSON
                       url(r'^getDSdata', getter.getTimeEvolutionPlotData, {'MView':'DS'      }, "getDSPlotData" ),
                       url(r'^getDTdata', getter.getTimeEvolutionPlotData, {'MView':'DataTier'}, "getDTPlotData" ),
                       url(r'^getDSNdata', getter.getTimeEvolutionPlotData, {'MView':'DSName'  }, "getDSNPlotData"),

                       url(r'^getSingleDSstat', getter.getDataSetStat, {}, "getSingleDSPlotStat" ),
                       url(r'^getSingleDTstat', getter.getDataTierStat, {}, "getSingleDTPlotStat" ),
                       url(r'^getSingleDNstat', getter.getProcessedDataSetStat, {}, "getSingleDSNPlotStat"),

                       # Tables JSON
                       url(r'^DSStatInTimeWindow/', getter.getDSStatInTimeWindow, {'MView':'DS'      }, "DSStatInTimeWindow"),
                       url(r'^DataTierStatInTimeWindow/', getter.getDSStatInTimeWindow, {'MView':'DataTier'}, "DataTierStatInTimeWindow"),
                       url(r'^DSNameStatInTimeWindow/', getter.getDSStatInTimeWindow, {'MView':'DSName'  }, "DSNameStatInTimeWindow"),
                       
                       url(r'^getUserStat/', getter.getUserStat, {}, "getUserStat"),
                       
                       url(r'^getCorruptedFiles/', getter.getCorruptedFiles, {'dbview': 'detail'     }, "getCorruptedFiles"),
                       url(r'^getCorruptedFilesSiteSummary/', getter.getCorruptedFiles, {'dbview': 'siteSummary'}, "getCorruptedFilesSiteSummary"),
                       url(r'^getCorruptedFilesDSSummary/', getter.getCorruptedFiles, {'dbview': 'dsSummary'  }, "getCorruptedFilesDSSummary"  ),

                       # Other JSON
                       url(r'^availableDataSets', getter.dataSets, {}, "dataSets"),
                       url(r'^availableDataTiers', getter.dataTiers, {}, "dataTiers"),
                       url(r'^availableProcessedDataSets', getter.processedDataSets, {}, "processedDataSets"),

                       # Documentation
                       url(r'^utility$', render.renderTemplate, {'tmplPath': 'popularity/utility.html'    }, "popularityutility"   ),
                       url(r'^versions$', render.renderTemplate, {'tmplPath': 'popularity/version_log.html'}, "popularityversionlog"),
                       url(r'^apidoc$', render.renderTemplate, {'tmplPath': 'popularity/apidoc.html'     }, "popularityapidoc"    ),
                       )

