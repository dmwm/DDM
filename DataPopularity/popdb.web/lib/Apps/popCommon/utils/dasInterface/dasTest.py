#! /usr/bin/env python26

"""
DAS query test program
"""
__author__ = "Nicolo Magini"

import logging
import sys
from optparse import OptionParser
from dasInterface import DASInterface

logger = logging.getLogger(__name__)

if  sys.version_info < (2, 6):
    raise Exception("DAS requires python 2.6 or greater")

class DASOptionParser:
    """
    DAS cache client option parser
    """
    def __init__(self):
        self.parser = OptionParser()
        self.parser.add_option("-v", "--verbose", action="store",
                               type="int", default=0, dest="verbose",
                               help="verbose output")
        self.parser.add_option("--query", action="store", type="string",
                               default=False, dest="query",
                               help="DAS QL query, mabdatory")
        self.parser.add_option("--host", action="store", type="string",
                               default='https://cmsweb.cern.ch', dest="host",
                               help="specify host name of DAS cache server, default https://cmsweb.cern.ch")
        self.parser.add_option("--idx", action="store", type="int",
                               default=0, dest="idx",
                               help="start index for returned DAS result set, aka pagination, use w/ limit")
        self.parser.add_option("--limit", action="store", type="int",
                               default=0, dest="limit",
                               help="number of returned DAS results (results per page)")

    def get_opt(self):
        """
        Returns parse list of options
        """
        return self.parser.parse_args()

def main():
    optmgr  = DASOptionParser()
    opts, _ = optmgr.get_opt()
    host    = opts.host
    debug   = opts.verbose
    query  = opts.query
    if not query:
        msg="--query option is mandatory"
        raise Exception(msg)
    idx     = opts.idx
    limit   = opts.limit
    myDas = DASInterface(debug=debug)
    logger.debug(query)
    data = myDas.get_das_data(host, query, idx, limit)
    logger.debug(data)
    
#
# main
#

if __name__ == '__main__':
    main()
