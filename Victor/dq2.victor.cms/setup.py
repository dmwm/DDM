#!/usr/bin/env python
import glob

from distutils.core import setup,Extension
from ConfigParser import ConfigParser

config = ConfigParser()
configFile = open('module.cfg')
config.readfp(configFile)
configFile.close()

setup(
    name         = config.get('module', 'name'),
    version      = config.get('module', 'version'),
    author       = config.get('module', 'author'),
    author_email = config.get('module', 'author_email'),
    description  = config.get('module', 'description'),
    url          = config.get('module', 'url'),

    packages=[
        'dq2',
        'dq2.common',
        'dq2.common.aspects',
        'dq2.common.cli',
        'dq2.common.python',
        'dq2.common.stomp',
        'dq2.common.testcase',
        'dq2.common.utils',
        'dq2.common.validator',
        'dq2.common.validator.testcase',
        'dq2.victor',
        'dq2.victor.cms',
        'dq2.victor.interface',
    ],
    
    package_dir={'': 'lib'},
    
    data_files=[
        ('/opt/dq2/etc/', ['config/dq2/etc/logging.cfg',
                           'config/dq2/etc/dq2.cfg']),
                               
        ('/etc/cron.d', ['config/cron.d/victor.agent.cms']),
                
    ]
    
)
