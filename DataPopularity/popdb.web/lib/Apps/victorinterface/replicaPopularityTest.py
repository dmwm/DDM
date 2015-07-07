#!/usr/bin/env python26
#pylint: disable-msg=C0301,C0103

"""
PopDB query script based on DAS command line tool by Valentin Kuznetsov
"""
from __future__ import absolute_import
__author__ = "Nicolo Magini"

import logging
import sys
import datetime
from .replicaPopularityBase import ReplicaPopularity

from   optparse import OptionParser

logger = logging.getLogger(__name__)

if  sys.version_info < (2, 6):
    raise Exception("DAS requires python 2.6 or greater")

class DASOptionParser:
    """
    DAS cache client option parser
    """
    def __init__(self):
        usage="%prog [options] SITENAME"
        self.parser = OptionParser(usage=usage)
        self.parser.add_option("-v", "--verbose", action="store",
                               type="int", default=0, dest="verbose",
                               help="verbose output")
        self.parser.add_option("--host", action="store", type="string",
                               default='https://cmsweb.cern.ch', dest="host",
                               help="specify host name of DAS cache server, default https://cmsweb.cern.ch")
        self.parser.add_option("--pophost", action="store", type="string",
                               default='http://cms-popularity-prod.cern.ch', dest="pophost",
                               help="specify host name of PopDB server, default http://cms-popularity-prod.cern.ch")
        self.parser.add_option("--incomplete", action="store", type="int",
                               default='0', dest="incomplete",
                               help="restrict to complete block replicas")
        self.parser.add_option("--tstart", action="store", type="string",
                               default=str(datetime.date.today()-datetime.timedelta(30)), dest="timestart",
                               help="specify starting time for popularity calculation, default is 30 days ago. NOTE: no data available more than 5 weeks ago")
        self.parser.add_option("--tstop", action="store", type="string",
                               default=str(datetime.date.today()), dest="timestop",
                               help="specify ending time for popularity calculation, default is today.")
    def get_opt(self):
        """
        Returns parse list of options
        """
        return self.parser.parse_args()
        
        
def main():
    """Main function"""
    optmgr  = DASOptionParser()
    opts, args = optmgr.get_opt()
    host    = opts.host
    pophost = opts.pophost
    debug   = opts.verbose
    incomplete = opts.incomplete
    timestart = opts.timestart
    timestop = opts.timestop
    try:
        sitename=args[0]
    except IndexError:
        raise Exception('You must provide input SITENAME')
    combiner = ReplicaPopularity(debug=debug, dasHost=host, popHost=pophost)
#    combiner.get_das_data(host, sitename, idx, limit)
#    combiner.get_pop_data(pophost, sitename, timestart, timestop)
    outdict = combiner.combine(sitename, timestart, timestop, incomplete, debug)
    logger.debug(outdict)
#
# main
#

if __name__ == '__main__':
    main()
                                                                                        
