#!/usr/bin/env python
import glob

from distutils.core import setup,Extension
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

    packages=['dashboard.popdb-cmssw','dashboard.popdb-cmssw.test',
              'dashboard.dao.oracle.xrootd'],

    package_dir={'': 'lib'},

    data_files=[
        ('etc/dashboard-dao', glob.glob('config/etc/dashboard-dao/*')),
        ('etc/dashboard-simplevisor', glob.glob('config/etc/dashboard-simplevisor/*')),
        ('etc/dashboard-service-config/cmssw-collector/etc',glob.glob('config/etc/dashboard-service-config/cmssw-collector/etc/*')),
        ('etc/dashboard-service-config/cmssw-listener/etc',glob.glob('config/etc/dashboard-service-config/cmssw-listener/etc/*')),
        ('etc/dashboard-service-config',glob.glob('config/etc/dashboard-service-config/*.cfg')),
        ('etc/dashboard-service-config',glob.glob('config/etc/dashboard-service-config/*.xml')),
        ('cron', ['config/cron/dashbServices.config']),
        ('db', glob.glob('config/db/*')),
        ('/etc/cron.d', ['config/cron/dashboard_service_config']),
   ]
    
)
