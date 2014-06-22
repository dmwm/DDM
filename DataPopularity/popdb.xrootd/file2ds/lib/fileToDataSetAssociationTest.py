#! /usr/bin/env python26

# Test main macro,


import os
import logging
import sys
from optparse import OptionParser
from fileToDataSetAssociation import fileToDataSetAssociator


__version__ = 0.1

if  sys.version_info < (2, 6):
    raise Exception("PHEDEX requires python 2.6 or greater")

def options():
    """
    Read options 
    """
    parser = OptionParser(version="%prog " + str(__version__))
    parser.add_option("-v", "--verbose", dest="verbose",
                      action="store_true", default=False,
                      help="Be more verbose")
    parser.add_option("-d", "--debug", dest="debug",
                      action="store_true", default=False,
                      help="print debugging statements")

    parser.add_option("-f", "--fake", dest="fakeUpload",
                      action="store_true", default=False,
                      help="doesn't upload the data into the DB - Just queries the dashboard for test")

    parser.add_option("--host", action="store", type="string",
                      default='https://cmsweb.cern.ch', dest="host",
                      help="specify host name of PHEDEX cache server, default https://cmsweb.cern.ch")

    
    options, args = parser.parse_args()
    
    return options


def main():
    config = options()
    fda = fileToDataSetAssociator(config)
    
    pid = os.getpid()
    fda.run(pid)

if __name__ == '__main__':
    main()
