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
sys.path.append('../stage/lib')

from dashboard.distutils.config import setup
#from distutils.core import setup,Extension

setup(
    packages=[
        'victor.monitoring.cms',
    ],
    
    package_dir={'': 'lib'},
    
    data_files=[
        ('bin', glob.glob('build/bin/*')),                
    ]
    
)