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

    packages=['', 'phedexInterface'],

    package_dir={'': 'lib'},

    data_files=[
        ('lib/', glob.glob('lib/*sh')),
        ('etc/', ['config/auth.txt']),
        ('/etc/cron.d', ['config/xrootd_popularity_file2ds']),
   ]
)
