"""
@copyright: European Organization for Nuclear Research (CERN)
@author: Fernando H. Barreiro U{fernando.harald.barreiro.megino@cern.ch<mailto:fernando.harald.barreiro.megino@cern.ch>}, CERN, 2011-2012
@license: Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at U{http://www.apache.org/licenses/LICENSE-2.0}
"""

#!/usr/bin/env python
import glob
import sys

from distutils.core import setup,Extension
from ConfigParser import ConfigParser

config = ConfigParser()
configFile = open('module.cfg')
config.readfp(configFile)
configFile.close()


#sys.path.append('../stage/lib')

setup(
    name         = config.get('module', 'name'),
    version      = config.get('module', 'version'),
    author       = config.get('module', 'author'),
    author_email = config.get('module', 'author_email'),
    description  = config.get('module', 'description'),
    url          = config.get('module', 'url'),

    packages=['',],
    
    package_dir={'': 'lib'},
    
    data_files=[
        ('templates'                    ,glob.glob('templates/*.html')),
        ('media/css/datatables'         ,glob.glob('media/css/datatables/*.css')),
        ('media/css/SpryMenuBar'        ,glob.glob('media/css/SpryMenuBar/*.css')),
        ('media/css/SpryMenuBar'        ,glob.glob('media/css/SpryMenuBar/*.gif')),
        ('media/css/ui-lightness'       ,glob.glob('media/css/ui-lightness/*.css')),
        ('media/css/ui-lightness/images',glob.glob('media/css/ui-lightness/images/*.png')),
        ('media/js'                     ,glob.glob('media/js/*.js')),
        ('media/images'                 ,glob.glob('media/images/*.png')),        
        ('media/images'                 ,glob.glob('media/images/*.gif')),        
        ('/var/www/html/images'         ,glob.glob('media/images/*.png')),
        ('/var/www/html/images'         ,glob.glob('media/images/*.gif')),
        ('/var/www/html'     ,['templates/index.html']),
        ('/etc/httpd/conf.d', ['config/pop_victor.conf']),
    ]
    
)
