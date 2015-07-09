"""
@copyright: European Organization for Nuclear Research (CERN)
@author: Fernando H. Barreiro U{fernando.harald.barreiro.megino@cern.ch<mailto:fernando.harald.barreiro.megino@cern.ch>}, CERN, 2011-2012
@license: Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at U{http://www.apache.org/licenses/LICENSE-2.0}
"""

from __future__ import absolute_import
from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import victor.views

urlpatterns = patterns('',
    (r'^accounting$', victor.views.accountingView),
    (r'^association_view/(?P<site>[*_a-zA-Z0-9./-]+)/(?P<group>[*_a-zA-Z0-9./-]+)$',  victor.views.associationView),
    (r'^site_view/(?P<site>[*_a-zA-Z0-9./-]+)$',  victor.views.siteView),
    (r'^get_blocks/(?P<info>[*_^a-zA-Z0-9./-]+)$', victor.views.getBlocksForDataset),
    (r'^about$',  victor.views.aboutView),
    (r'', victor.views.invalidView),
    )
