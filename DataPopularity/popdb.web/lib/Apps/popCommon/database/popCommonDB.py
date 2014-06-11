""" Module for the connection with the Popularity database
Contains functions commonly needed by Popularity apps"""

from django.db import connection, connections
from Apps.popCommon.utils import utility
from Apps.popCommon.PopularityException import PopularityDBException
from Apps.popCommon.utils.confSettings import confSettings
import logging

logger = logging.getLogger(__name__)

popsettings = confSettings()
#DBUSER = popsettings.getSetting("popCommon", "DBUSER")
#DBUSER = 'CMS_POPULARITY_SYSTEM'

def getSitesList(DB): 
    """ Query the memorized view MV_Site to get a list of
    the sites present on the database"""
   
    table = "%s.%s" % (DB, "MV_Site")    

    query = 'select SITENAME from %s order by SITENAME' % (table)    
    try:
        cursor = connections[DB].cursor()
        cursor.execute(query)

        data = {}
        data = utility.genericTranslateInList(cursor)
        sitelist = map(lambda x: x["SITENAME"], data)
        return sitelist
    
    except Exception as e:
        raise PopularityDBException(query, e)

def getDataTierList(DB):
    """ Query the memorized view MV_DATATIER to get a list of
    the DataTier present on the database"""

    table = "%s.%s" % (DB, "MV_DATATIER")
    query = 'select COLLNAME from  %s' % (table)
    
    try:
        cursor = connections[DB].cursor()
        cursor.execute(query)

        data = {}
        data = utility.genericTranslateInList(cursor)
        """
        dtlist = map(lambda x: x["COLLNAME"], data)
        """
        return data 
    
    except Exception as e:
        raise PopularityDBException(query, e)


def getDataSetList(DB):
    """ Query the memorized view MV_DS to get a list of
    the DataSets present on the database"""

    table = "%s.%s" % (DB, "MV_DS")
    query = 'select COLLNAME from  %s' % (table)

    try:
        cursor = connections[DB].cursor()
        cursor.execute(query)

        data = {}
        data = utility.genericTranslateInList(cursor)
        """
        dslist = map(lambda x: x["COLLNAME"], data)
        """
        return data

    except Exception as e:
        raise PopularityDBException(query, e)

def getProcessedDataSetList(DB):
    """ Query the memorized view MV_DSNAME to get a list of
    the Processed DataSets present on the database"""

    table = "%s.%s" % (DB, "MV_DSNAME")
    query = 'select COLLNAME from  %s' % (table)

    try:
        cursor = connections[DB].cursor()
        cursor.execute(query)

        data = {}
        data = utility.genericTranslateInList(cursor)
        """
        dslist = map(lambda x: x["COLLNAME"], data)
        """
        return data

    except Exception as e:
        raise PopularityDBException(query, e)
