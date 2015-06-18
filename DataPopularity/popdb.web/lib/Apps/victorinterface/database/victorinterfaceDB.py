from django.db import connection, connections, transaction
from Apps.victorinterface.utils import victorinterfaceUtility
from Apps.popCommon.PopularityException import PopularityDBException, Paramvalidationexception
from datetime import datetime, date, timedelta

import logging

logger = logging.getLogger(__name__)

"""
TODO: insert query to xrootd database in case of params.source == 'xrootd'
"""
#-------------------------------------------------------------------------------------------------------
# This is the new victor query, that returns the collection accessed at least
# once in the past days (configurable up to 5 weeks in the past)
# organized per site, with additional CPU and nAcc stats

def WhatInSiteWithStat(collType, params):
    
    data = []

    logger.info('Using access data source: %s' % params.source)
    DBUSER = 'CMS_POPULARITY_SYSTEM'
    if params.source == 'xrootd':
        DBUSER = 'CMS_EOS_POPULARITY_SYSTEM'

    logger.info('Using DBUSER: %s' % DBUSER)

    ### D.G. Comment [2014-03-18] request to cover also the last 12 months, moving to MV MV_block_stat0_aggr_12_months
    ### D.G. Comment: MV_block_stat0_aggr_5_weeks is included in MV_block_stat0_aggr_180_days. Going to use only this
    #table_name = 'MV_block_stat0_aggr_5_weeks'
    #delta = datetime.strptime(params.TStop,"%Y-%m-%d") - datetime.strptime(params.TStart,"%Y-%m-%d")
    #if delta.days > 35:
    table_name = 'MV_block_stat0_aggr_12_months'

    #logger.info('Using MV %s' %table_name)

    vars = "SITENAME, COLLNAME"
    if  collType == 'BlocksStat':
        table = "%s.%s" % (DBUSER, table_name)
        vars+=", sum(TOTCPU) as TOTCPU, sum(NUMACCESSES) as NACC" 
    else:
        return {}

    whereCondition = "TDay >= trunc(to_date('%s','YYYY-MM-DD'),'W') and TDay <= trunc(to_date('%s','YYYY-MM-DD'),'W') " % (params.TStart, params.TStop)
    whereCondition+=" and SiteName like %s" % '%s'

    groupBy='sitename, collname'
    orderBy='sitename'
    query = "select %s from %s where %s group by %s order by %s;" % (vars, table, whereCondition, groupBy, orderBy)
    logger.info("WhatInSiteWithStat query: %s" % query)

    try:
        cursor = connections[DBUSER].cursor()
        cursor.execute(query, [params.SiteName])
        data= victorinterfaceUtility.genericTranslateInListDictVict(cursor, 'SITENAME', 'COLLNAME')
#        data=_genericTranslateInListDict(cursor,'COLLNAME','SITENAME')
            
    except Exception as e:
        raise PopularityDBException(query, e)

    return data

def WhatInSiteWithStatLastAcc(collType, params):
    data = []

    logger.info('Using access data source: %s' % params.source)
    DBUSER = 'CMS_POPULARITY_SYSTEM'
    if params.source == 'xrootd':
        DBUSER = 'CMS_EOS_POPULARITY_SYSTEM'

    logger.info('Using DBUSER: %s' % DBUSER)

    applyPatch = False
    if (params.SiteName == 'T2_CH_CERN' or params.SiteName == 'T0_CH_CERN') and params.source != 'xrootd' :
        applyPatch = True
        logger.info('applying patch to cope with the fact sitename in crab monitoring for CH_CERN moved from T0 to T2 in Apr 2013, affecting popularity statistics')

    vars = "SITENAME, COLLNAME, (tday - to_date('1970-01-01','YYYY-MM-DD')) * 86400 as LASTDAY"
    table = "%s.%s" % (DBUSER, 'MV_block_stat0_last_access')
    whereCondition =" SiteName like %s" % '%s'
    query = "select %s from %s where %s" % (vars, table, whereCondition)

    if applyPatch:
        query = "select 'T2_CH_CERN' as SITENAME, COLLNAME, max(tday - to_date('1970-01-01','YYYY-MM-DD')) * 86400 as LASTDAY from " + table + " where SITENAME = 'T0_CH_CERN' or SITENAME = 'T2_CH_CERN' group by COLLNAME"
    logger.info('WhatInSiteWithStatLastAcc query: %s'% query)
    # -----------------------------------

    try:
        cursor = connections[DBUSER].cursor()
        if applyPatch:
            cursor.execute(query)
        else:
            cursor.execute(query, [params.SiteName])
        data= victorinterfaceUtility.genericTranslateInListDictVict(cursor, 'SITENAME', 'COLLNAME')
        
    except Exception as e:
        raise PopularityDBException(query, e)

    return data

def AccessStatsByDirAtSite(params):
    # Provides access statistics aggregated by directory
    # Requires parameters SiteName and DirName (the top-level dir from which to provide the statistics)
    # Currently only supported for xrootd popularity at T2_CH_CERN (EOS)
    
    data = {}

    logger.info('Using access data source: %s' % params.source)
    if params.source == 'xrootd':
        DBUSER = 'CMS_EOS_POPULARITY_SYSTEM'
    else:
        raise Paramvalidationexception('source', 'param source=%s unsupported, please select source=xrootd' % params.source)

    logger.info('Using DBUSER: %s' % DBUSER)

    vars = "'T2_CH_CERN' as SITENAME, regexp_replace(PATH,'^/eos/cms','') as PATH, (max_tday - to_date('1970-01-01','YYYY-MM-DD')) * 86400 as LASTDAY, (min_tday - to_date('1970-01-01','YYYY-MM-DD')) * 86400 as FIRSTDAY,  READ_ACC as NACC, READ_BYTES as READMBYTES"
    table = "%s.%s" % (DBUSER, 'V_XRD_STAT2_AGGR1')
    whereCondition =" 'T2_CH_CERN' like %s and regexp_replace(PATH,'^/eos/cms','') like %s" % ('%s', '%s')

    query = "select %s from %s where %s" % (vars, table, whereCondition)

    logger.info('AccessStatsByDirAtSite query: %s'% query)

    # -----------------------------------

    try:
        cursor = connections[DBUSER].cursor()

        # For wildcard queries, we need to add the % wildcard in the bind variable...
        cursor.execute(query, [params.SiteName, params.DirName+'%'])

        data = victorinterfaceUtility.genericTranslateInListDictVict(cursor, 'SITENAME', 'PATH')
        
    except Exception as e:
        raise PopularityDBException(query, e)

    return data
