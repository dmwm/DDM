from __future__ import print_function
import os
import sys
print(sys.version_info)

import django.core.handlers.wsgi

path = '/var/www/DjangoProjects/'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'victor.settings'

application = django.core.handlers.wsgi.WSGIHandler()
