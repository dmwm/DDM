from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^', include('Apps.popularity.urls')),
    url(r'^popularity/', include('Apps.popularity.urls')),
    url(r'^xrdpopularity/', include('Apps.xrdPopularity.urls')),
    url(r'^victorinterface/', include('Apps.victorinterface.urls')),
)
