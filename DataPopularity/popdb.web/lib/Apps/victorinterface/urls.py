from django.conf.urls import *
import views as views

urlpatterns = patterns('',

                       url(r'^$', views.index, {}, 'victorinterfaceindex'),

                       #---------------------------------------------
                       #Links for the Data Reduction Agent
                       #---------------------------------------------


                       url(r'^accessedBlocksStat/$', views.getCollectionInSiteWithStat, {'collType':'BlocksStat'}, 'accessedBlocksStat'),
                       url(r'^accessedBlocksStatLastAcc/$', views.getCollectionInSiteWithStat, {'collType':'BlocksStat', 'lastAcc': True}, 'accessedBlocksStatLastAcc'),

                       url(r'^popdbcombine/$', views.getCombinedDASPopInfo, {}, 'popdbcombine'),
                       url(r'^popdbcombineLastAcc/$', views.getCombinedDASPopInfo, {'lastAcc': True}, 'popdbcombineLastAcc'),

                       url(r'^accessedDirsStat$', views.getDirsInSiteWithStat, {}, 'accessedDirsStat'),

                       )
