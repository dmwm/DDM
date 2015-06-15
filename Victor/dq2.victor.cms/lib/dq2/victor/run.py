"""
Main module 

@copyright: European Organization for Nuclear Research (CERN)
@author: Fernando H. Barreiro U{fernando.harald.barreiro.megino@cern.ch<mailto:fernando.harald.barreiro.megino@cern.ch>}, CERN, 2011
@license: Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at U{http://www.apache.org/licenses/LICENSE-2.0}
"""
from optparse import OptionParser
from dq2.victor.victor import Victor

parser = OptionParser()
parser.add_option('-c', '--conf', type='string', dest='config', default='/opt/dq2/etc/dq2.cfg',
                  help='Path to the configuration to be used by victor.')

(options, args) = parser.parse_args()

victor = Victor('victor', options.config)
victor.run()
