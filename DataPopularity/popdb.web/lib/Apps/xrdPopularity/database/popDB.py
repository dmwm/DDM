from django.db import connection, connections
from Apps.popCommon.utils import utility
from Apps.popCommon.PopularityException import PopularityDBException

import logging

logger = logging.getLogger(__name__)

DBUSER = 'CMS_EOS_POPULARITY_SYSTEM'
#DBUSER = 'EOS_POPULARITY_SYSTEM_ATL'


def xrdStatInTimeWindow(params):

    table = "%s.%s" % (DBUSER, params.table)
        
    vars  = 'xTime, yValue, yValue/3600. as rate, round((xTime-to_date(\'19700101\',\'YYYYMMDD\'))*86400)*1000 as millisecondsSinceEpoch'

    whereCondition = '''
    xTime >= to_date(\'%s\',\'YYYY-MM-DD HH24:MI:SS\') 
    and xTime <= to_date(\'%s\',\'YYYY-MM-DD HH24:MI:SS\')''' % (params.TStart, params.TStop)

    orderby = ''
    if hasattr(params, 'orderby'):
        orderby = params.orderby
    
    query = 'select %s from %s where %s %s' % (vars, table, whereCondition, orderby)

    logger.info(query) 
    try:
        cursor = connections[DBUSER].cursor()
        cursor.execute(query)
        
    except Exception as e:
        raise PopularityDBException(query, e)

    data = {}
    data['DATA'] = utility.genericTranslateInList(cursor)
    return data
    
    
    
# ------------------------------------------------------------


def DSStatInTimeWindow(params):
    
    #cursor = connection.cursor()
    if params.table == 'DataTier':
        table = "%s.%s" % (DBUSER, "MV_XRD_DS_STAT0_AGGR2")
    elif params.table == 'DS':
        table = "%s.%s" % (DBUSER, "MV_XRD_DS_STAT0_AGGR1")
    elif params.table == 'DSName':
        table = "%s.%s" % (DBUSER, "MV_XRD_DS_STAT0_AGGR4")
    elif params.table == 'UserDS':
        table = "%s.%s" % (DBUSER, "MV_XRD_DS_STAT1_AGGR1")

    vars  = '''collName , sum(numAccesses) as nAcc, round(sum(totCPU)/3600,0) 
             as totCPU, sum(numUsers)/( to_date('%s','YYYY-MM-DD') - to_date('%s','YYYY-MM-DD') +1  ) as nUsers,
             sum(readBytes)/1024/1024 / sum(numAccesses) as readMB
             ''' % (params.TStop, params.TStart)
    
    whereCondition = '''TDay >= to_date('%s','YYYY-MM-DD') 
                        and TDay <= to_date('%s','YYYY-MM-DD')
                        and isUserCMS = %s
                     ''' % (params.TStart, params.TStop, params.isUserCMS)
    groupBy  = "collName" 

    orderBy  = "%s desc" % params.orderVar
    
    if hasattr(params, "collname"):
       whereCondition += " and collName = '%s'" % (params.collname)
    
    # if params.SiteName != 'summary':
    #     groupBy = "%s, siteName" % groupBy 
    #     whereCondition = "%s and siteName like '%s' " % (whereCondition, params.SiteName)
    # else:
    #     table += "_SUMM"
            
    query = '''select collName, nAcc, totcpu, nUsers, readMB,
             100* ratio_to_report(nAcc)   over() as rnAcc ,
             100* ratio_to_report(totcpu) over() as rtotcpu ,
             100* ratio_to_report(nUsers) over() as rnUsers ,
             100* ratio_to_report(readMB) over() as rreadMB
             from (select %s from %s where %s group by %s order by %s)
            ''' % (vars, table, whereCondition, groupBy, orderBy)

    logger.info(query) 
    try:
        cursor = connections[DBUSER].cursor()
        cursor.execute(query)

    except Exception as e:
        raise PopularityDBException(query, e)


    data = {}
    data['DATA'] = utility.genericTranslateInList(cursor)
    return data
    
    
    
# ------------------------------------------------------------
    
    
    
def MostPopDSStat(params):

    #cursor = connection.cursor()

    if params.table == 'DataTier':
        table = "%s.%s" % (DBUSER, "MV_XRD_DS_STAT0_AGGR2")
    elif params.table == 'DS':
        table = "%s.%s" % (DBUSER, "MV_XRD_DS_STAT0_AGGR1")
    elif params.table == 'DSName':
        table = "%s.%s" % (DBUSER, "MV_XRD_DS_STAT0_AGGR4")
    elif params.table == 'UserDS':
        table = "%s.%s" % (DBUSER, "MV_XRD_DS_STAT1_AGGR1")

    #TimeFormats: timeformat acts to the displayed date, timeformatTrunc acts to the truncation of the input dates, and should be keept with the format of the aggregation

    timeformat = 'YYYY/MM/DD'

    if params.AggrFlag == 'day':
        timeformatTrunc = 'DDD'
    elif params.AggrFlag == 'week':
        timeformatTrunc = 'WW'
    elif params.AggrFlag == 'month':
        timeformatTrunc = 'MONTH'
    elif params.AggrFlag == 'quarter':
        timeformatTrunc = 'Q'
    elif params.AggrFlag == 'year':
        timeformatTrunc = 'YEAR'

    whereCondition = '''collName = \'%s\'
                      and isUserCMS = %s
                     ''' % (params.collName, params.isUserCMS)
    orderBy       = "TDay " 
    vtime         = "trunc(TDay,'%s')" % (timeformatTrunc)
    
    groupBy = "group by %s, collName" % vtime
    vars  = ''' %s as TDay, sum(numAccesses) as naccess, 
               round(sum(totCPU)/3600,0) as totCPU,
               sum(numUsers) as nUsers
            ''' % (vtime)
    
    #if params.SiteName != 'summary':
    #    whereCondition = "%s and siteName like '%s' " % (whereCondition, params.SiteName)
    #else:
    #    table += "_SUMM"
        
    query = "select %s from %s where %s %s " % (vars, table, whereCondition, groupBy)
    query = '''select round((
               TDay-to_date(\'19700101\',\'YYYYMMDD\')
               )*86400)*1000
               as millisecondsSinceEpoch,
               ta.%s
               from ( %s ) ta order by %s''' % (params.orderVar, query, orderBy)

    logger.info(query)         
    try:
        cursor = connections[DBUSER].cursor()
        cursor.execute(query)

    except Exception as e:
        raise PopularityDBException(query, e)


    data = {'data': [(utility.assignValue(row[0]), utility.assignValue(row[1])) for row in cursor.fetchall() ],
            'name': params.collName}
    return data


#-------------------------------------------------------------------------------

def UserStatInTimeWindow(params):

    #cursor = connection.cursor()
    
    table = "%s.%s" % (DBUSER, "MV_XRD_DS_STAT0_AGGR3")

    orderBy  = "%s " % params.orderVar
    
    if hasattr(params, 'LocalVsGlobal') and params.LocalVsGlobal == True :

        whereCondition = '''TDay >= to_date('%s','YYYY-MM-DD') 
                            and TDay <= to_date('%s','YYYY-MM-DD') 
                            ''' % (params.TStart, params.TStop)

        groupBy  = "REGEXP_INSTR(server_username,'^cms'), collName" 

        query = '''select replace(replace(username,\'0\',\'Local\'),\'1\',\'Grid\') as username, collName, nAcc, totcpu, readMB,
                   100* ratio_to_report(nAcc) over() as rnAcc ,
                   100* ratio_to_report(totcpu) over() as rtotcpu, 
                   100* ratio_to_report(readMB) over() as rreadMB
                   from (select REGEXP_INSTR(server_username,\'^cms\') as username, collName, sum(numAccesses) as nAcc, round(sum(totcpu)/3600.,3) as totcpu, sum(readBytes)/1024/1024 / sum(numAccesses) as readMB 
                   from %s where %s group by %s order by %s) 
                 ''' % (table, whereCondition, groupBy, orderBy) 
        
    else:
        whereCondition = '''TDay >= to_date('%s','YYYY-MM-DD') 
                            and TDay <= to_date('%s','YYYY-MM-DD')''' % (params.TStart, params.TStop)

        if params.collName.lower() != 'all' :
            whereCondition += '''and collName like '%s' ''' % params.collName


        groupBy  = "server_username" 

            
        query = '''select username, nAcc, totcpu, readMB,
        100* ratio_to_report(nAcc) over() as rnAcc ,
        100* ratio_to_report(totcpu) over() as rtotcpu, 
        100* ratio_to_report(readMB) over() as rreadMB
        from (select server_username as username, sum(numAccesses) as nAcc, round(sum(totcpu)/3600.,3) as totcpu, sum(readBytes)/1024/1024 / sum(numAccesses) as readMB 
        from %s where %s group by %s order by %s) ''' % (table, whereCondition, groupBy, orderBy) 

        
    logger.info(query) 
    try:
        cursor = connections[DBUSER].cursor() 
        cursor.execute(query)#

    except Exception as e:
        raise PopularityDBException(query, e)    


    data = {}
    data['DATA'] = utility.genericTranslateInList(cursor)
    return data
    
    
#------------------------------------------------------------------------------------
