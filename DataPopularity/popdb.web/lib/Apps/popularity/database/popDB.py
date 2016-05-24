from django.db import connection
from Apps.popCommon.utils import utility
from Apps.popCommon.PopularityException import PopularityDBException
from Apps.popCommon.utils.confSettings import confSettings
import logging

logger = logging.getLogger(__name__)
popsettings = confSettings()
DBUSER = popsettings.getSetting("popCommon", "DBUSER")
#DBUSER = 'CMS_POPULARITY_SYSTEM'

def DSStatInTimeWindow(params, MView):
    
    #cursor = connection.cursor()
    if params.includeWMAgent == 'y':
        baseMV = "STAT0"
    elif params.includeWMAgent == 'n':
        baseMV = "STAT1"

    if MView == 'DataTier':
        aggrMV = "AGGR2"
    elif MView == 'DS':
        aggrMV = "AGGR1"
    elif MView == 'DSName':
        aggrMV = 'AGGR4'

    table = "%s.MV_DS_%s_%s" % (DBUSER, baseMV, aggrMV)
    
    vars  = '''collName , sum(numAccesses) as nAcc, round(sum(totCPU)/3600,0) 
             as totCPU, sum(numUsers) as nUsers''' 
    whereCondition = '''TDay >= to_date('%s','YYYY-MM-DD') 
                        and TDay <= to_date('%s','YYYY-MM-DD')
                     ''' % (params.TStart, params.TStop)
    groupBy  = "collName" 

    if params.orderVar == 'naccess' :    
        orderBy  = "nAcc desc"
    elif params.orderVar == 'nusers' :    
        orderBy  = "nUsers desc"
    else:
        orderBy  = "totCPU desc"
    
    if hasattr(params, "collname"):
       whereCondition += " and collName = '%s'" % (params.collname)
    
    if params.SiteName != 'summary':
        groupBy = "%s, siteName" % groupBy 
        whereCondition = "%s and siteName like '%s' " % (whereCondition, params.SiteName)
    else:
        table += "_SUMM"
            
    query = '''select collName, nAcc, totcpu, nUsers, 100* ratio_to_report(nAcc) 
             over() as rnAcc , 100* ratio_to_report(totcpu) 
             over() as rtotcpu , 100* ratio_to_report(nUsers) 
             over() as rnUsers 
             from (select %s from %s where %s group by %s order by %s)
            ''' % (vars, table, whereCondition, groupBy, orderBy)

    logger.info(query) 
    try:
        cursor = connection.cursor()
        cursor.execute(query)

    except Exception as e:
        raise PopularityDBException(query, e)


    data = {}
    data['DATA'] = utility.genericTranslateInList(cursor)
    return data
    
    
    
# ------------------------------------------------------------
    
    
    
def MostPopDSStat(params, MView, collName):

    #cursor = connection.cursor()

    if params.includeWMAgent == 'y':
        baseMV = "STAT0"
    elif params.includeWMAgent == 'n':
        baseMV = "STAT1"

    if MView == 'DataTier':
        aggrMV = "AGGR2"
    elif MView == 'DS':
        aggrMV = "AGGR1"
    elif MView == 'DSName':
        aggrMV = 'AGGR4'

    table = "%s.MV_DS_%s_%s" % (DBUSER, baseMV, aggrMV)
    
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

    whereCondition = "collName = '%s'" % collName
    orderBy       = "order by TDay " 
    vtime         = "trunc(TDay,'%s')" % (timeformatTrunc)
    
    groupBy = "group by %s, collName" % vtime
    vars  = '''to_char(%s,'%s') as TDay, sum(numAccesses) as nAcc, 
               round(sum(totCPU)/3600,0) as totCPU, sum(numUsers) as nUsers
            ''' % (vtime, timeformat)
    
    if params.SiteName != 'summary':
        whereCondition = "%s and siteName like '%s' " % (whereCondition, params.SiteName)
    else:
        table += "_SUMM"
        
    query = "select %s from %s where %s %s %s " % (vars, table, whereCondition, groupBy, orderBy)
        
    try:
        cursor = connection.cursor()
        cursor.execute(query)

    except Exception as e:
        raise PopularityDBException(query, e)


    data = {}
    data = {'DATA': utility.genericTranslateInList(cursor), 'COLLNAME': collName}
    return data


#-------------------------------------------------------------------------------


def UserStatInTimeWindow(params):

    #cursor = connection.cursor()
    
    table = "%s.%s" % (DBUSER, "MV_DS_STAT0_AGGR3")

    vars  = '''userid, sum(numAccesses) as nAcc, 
               round(sum(totCPU)/3600,0) as totCPU, 
               sum(numSites)/((to_date('%s','YYYY-MM-DD')-to_date('%s','YYYY-MM-DD'))+1) as nSites
            '''  % (params.TStop, params.TStart)
    whereCondition = '''TDay >= to_date('%s','YYYY-MM-DD') 
                        and TDay <= to_date('%s','YYYY-MM-DD') 
                     ''' % (params.TStart, params.TStop)

    if params.CollName.lower() != 'all' :
        whereCondition += '''and collName like '%s' ''' % params.CollName

    groupBy  = "userid" 

    if params.orderVar == 'nacc' :    
        orderBy  = "nAcc desc"
    elif params.orderVar == 'nsites' :    
        orderBy  = "nSites desc"
    else:
        orderBy  = "totCPU desc"
        
    useridtable = "%s.%s" % (DBUSER, "MV_USER_USERID")

    #NB: the additional group by username at the end of this query is needed because I discovered
    ##   that the unicity userid <-> username is not guarantee: the same username can have more than one userid in dashboard
    ##   the usage of userid was decided to help in making a query faster: being based on a integer search instead of a string search
    
    query = '''select username, nAcc, nsites, totcpu, 100* ratio_to_report(nAcc) 
               over() as rnAcc , 100* ratio_to_report(nsites) 
               over() as rnsites , 100* ratio_to_report(totcpu) 
               over() as rtotcpu 
               from (select username, sum(nacc) as nAcc, sum(nsites) as nsites, sum(totcpu) as totcpu 
               from %s, (select %%s from %%s where %%s group by %%s ) res 
               where %s.userid=res.userid group by username order by %%s )
             ''' % (useridtable, useridtable)

    query = query % (vars, table, whereCondition, groupBy, orderBy) 
    
    try:
        cursor = connection.cursor() 
        cursor.execute(query)
    
    except Exception as e:
        raise PopularityDBException(query, e)    


    data = {}
    data['DATA'] = utility.genericTranslateInList(cursor)
    return data
    
    
#------------------------------------------------------------------------------------


def CorruptedFilesInTimeWindow(params):
    
    if params.SiteName == 'summary':
        sitename = 'T2_%'
    else:
        sitename = params.SiteName

    #cursor = connection.cursor()
    
    table = "%s.%s" % (DBUSER, params.dbview)

    query = '''select * from %s 
    where sitename like %%s ;''' % (table)

    try:
        cursor = connection.cursor()
        cursor.execute(query, [sitename])

    except Exception as e:
        raise PopularityDBException(query, e)

    
    data = {}
    data['DATA'] = utility.genericTranslateInList(cursor)
    return data



