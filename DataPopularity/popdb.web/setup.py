"""
@copyright: European Organization for Nuclear Research (CERN)
@author: Domenico Giordano {domenico.giordano@cern.ch <mailto:domenico.giordano@cern.ch>}, CERN
@license: Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at U{http://www.apache.org/licenses/LICENSE-2.0}
"""
#!/usr/bin/env python
import glob

from distutils.core import setup, Extension
from ConfigParser import ConfigParser

config = ConfigParser()
configFile = open('module.cfg')
config.readfp(configFile)
configFile.close()

setup(
    name               = config.get('module', 'name'),
    version            = config.get('module', 'version'),
    author             = config.get('module', 'author'),
    author_email       = config.get('module', 'author_email'),
    description        = config.get('module', 'description'),
    long_description   = config.get('module', 'long_description'),
    url                = config.get('module', 'url'),

    packages=['',
              'Apps',
              'Apps.popCommon',
              'Apps.popCommon.database',
              'Apps.popCommon.utils',
              'Apps.popCommon.utils.dasInterface',
              'Apps.popularity',
              'Apps.popularity.database',
              'Apps.popularity.utils',
              'Apps.popularity.views',
              'Apps.xrdPopularity',
              'Apps.xrdPopularity.database',
              'Apps.xrdPopularity.utils',
              'Apps.xrdPopularity.views',
              'Apps.victorinterface',
              'Apps.victorinterface.database',
              'Apps.victorinterface.utils',
              'Apps.victorinterface.views',
              ],

    package_dir={'': 'lib'},

    data_files=[
        ('lib/Apps/popCommon/template', glob.glob('lib/Apps/popCommon/template/*.html')),
        ('lib/Apps/popularity/template/popularity', glob.glob('lib/Apps/popularity/template/popularity/*.html')),
        ('lib/Apps/xrdPopularity/template/xrdPopularity', glob.glob('lib/Apps/xrdPopularity/template/xrdPopularity/*.html')),
        ('lib/Apps/victorinterface/template/victorinterface', glob.glob('lib/Apps/victorinterface/template/victorinterface/*.html')),
 
        ('media/css/', glob.glob('media/css/*.css')),
        ('media/css/SpryMenuBar', glob.glob('media/css/SpryMenuBar/*.gif')),
        ('media/css/SpryMenuBar', glob.glob('media/css/SpryMenuBar/*.css')),
        ('media/css/table', glob.glob('media/css/table/*.css')),
        ('media/css/ui-lightness', glob.glob('media/css/ui-lightness/*css')),
        ('media/css/ui-lightness/images', glob.glob('media/css/ui-lightness/images/*png')),
        ('media/js/', glob.glob('media/js/*js')),
        ('media/js/calendar/', glob.glob('media/js/calendar/*js')),
        ('media/js/modules/', glob.glob('media/js/modules/*js')),
        ('media/js/table/', glob.glob('media/js/table/*js')),
        ('media/popularity/js/', glob.glob('media/popularity/js/*js')),
        ('media/xrdPopularity/js/', glob.glob('media/xrdPopularity/js/*js')),
        ('media/images/table/', glob.glob('media/images/table/*')),
        ('media/images/calendar/', glob.glob('media/images/calendar/*')),
        ('media/images/', glob.glob('media/images/*.*')),
        ('media/src/', glob.glob('media/src/*.py.txt')),
        ('/var/www/html/images', glob.glob('media/images/intro/*.png')),
        ('/var/www/html/images', glob.glob('media/images/intro/*.gif')),
        ('/var/www/html', ['lib/Apps/popCommon/template/intro/index.html']),
        ('/etc/httpd/conf.d', ['config/pop_web.conf']),
        ('etc/', glob.glob('config/*.ini')),

   ]
    
)
