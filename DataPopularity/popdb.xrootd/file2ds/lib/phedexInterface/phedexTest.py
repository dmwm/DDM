#! /usr/bin/env python26

# Test main macro, that uses the PHEDEXInterface to extract information
# about files, blocks, datasets
# Some examples of queries
#
# 1) python2.6 phedexTest.py --query='file=/store/hidata/HIRun2011/HIMinBiasUPC/RECO/PromptReco-v1/000/182/798/5C216A1E-EE1E-E111-91CF-0025901D627C.root'
#
# 2) python2.6 phedexTest.py --query='block=/HIMinBiasUPC/HIRun2011-PromptReco-v1/RECO#70c2b700-17cf-11e1-b723-003048caaace'
#
# 3) python2.6 phedexTest.py --query='dataset=/HIMinBiasUPC/HIRun2011-PromptReco-v1/RECO'



from __future__ import print_function
import logging
import sys
from optparse import OptionParser
from phedexRequest import PHEDEXInterface

logger = logging.getLogger(__name__)

if  sys.version_info < (2, 6):
    raise Exception("PHEDEX requires python 2.6 or greater")

class PHEDEXOptionParser:
    """
    PHEDEX cache client option parser
    """
    def __init__(self):
        self.parser = OptionParser()
        self.parser.add_option("-v", "--verbose", action="store",
                               type="int", default=0, dest="verbose",
                               help="verbose output")
        self.parser.add_option("--query", action="store", type="string",
                               default=False, dest="query",
                               help="PHEDEX QL query, mabdatory")
        self.parser.add_option("--host", action="store", type="string",
                               default='https://cmsweb.cern.ch', dest="host",
                               help="specify host name of PHEDEX cache server, default https://cmsweb.cern.ch")
        self.parser.add_option("--idx", action="store", type="int",
                               default=0, dest="idx",
                               help="start index for returned PHEDEX result set, aka pagination, use w/ limit")
        self.parser.add_option("--limit", action="store", type="int",
                               default=0, dest="limit",
                               help="number of returned PHEDEX results (results per page)")

    def get_opt(self):
        """
        Returns parse list of options
        """
        return self.parser.parse_args()

def main():
    optmgr  = PHEDEXOptionParser()
    opts, _ = optmgr.get_opt()
    host    = opts.host
    debug   = opts.verbose
    query  = opts.query
    if not query:
        msg="--query option is mandatory"
        raise Exception(msg)
    idx     = opts.idx
    limit   = opts.limit
    myPhedex = PHEDEXInterface(debug=debug)
    logger.debug(query)
    print('query \n' , query)
    data = myPhedex.get_phedex_data(host,query)
    logger.debug(data)
    print(' ')
    print('final result\n' , data)

#
# main
#

if __name__ == '__main__':
    main()
