#!/usr/bin/env python26
#pylint: disable-msg=C0301,C0103

"""
API to combine replica information from DAS and popularity from PopDB, and returning a dictionary of all block
replicas at site with associated popularity
"""
__author__ = "Nicolo Magini"

import logging
from replicaPopularityBase import ReplicaPopularity
from Apps.popCommon.utils.confSettings import confSettings


logger = logging.getLogger(__name__)

def replicaPopularity(opts):
    popsettings = confSettings()
    dasHost = popsettings.getSetting("victorinterface", "DATASERVICE_HOST")
    popHost = popsettings.getSetting("victorinterface", "POPULARITY_HOST")
    #dasHost = 'https://cmsweb.cern.ch'
    #popHost = 'http://cms-popularity-prod.cern.ch'
    debug   = 0
    sitename = opts.SiteName
    incomplete = 0 #opts.incomplete
    timestart = opts.TStart
    timestop = opts.TStop
    
    if  not sitename:
        raise Exception('You must provide input sitename')
    combiner = ReplicaPopularity(debug=debug,dasHost=dasHost,popHost=popHost)
    outdict = combiner.combine(sitename, timestart, timestop, incomplete, debug)
    logger.debug(outdict)
    return outdict
