"""
Module that contain common utility functionaliti for
all Popularity apps
"""

from datetime import datetime, date, timedelta
from decimal import Decimal


def assignValue(val):
    if isinstance(val, datetime):
        #hasattr(val, 'isoformat'):
        return val.isoformat(' ')
    elif isinstance(val, Decimal):
        return "%.1f" % float(val)
    else:
        return val

def genericTranslateInList(cursor):
    """
    Translate a query cursor into a list of result row
    """
    keys = [ row[0] for row in cursor.description]

    data = []
    for row in cursor.fetchall():
        values  = ( val for val in row  )
        dic={}
        for key, val in zip(keys,values):
            dic[key] = assignValue(val)
        data.append(dic)
    return data



"""
def genericTranslateInList(cursor):

    key = []
    for row in cursor.description:
        key.append(row[0])

    data = []
    for row in cursor.fetchall():
        i = 0
        dic = {}
        for val in row:
            if isinstance(val, Decimal):
                dic[key[i]] = "%.1f" % float(val)
            else:
                dic[key[i]] = val
            i += 1
        data.append(dic.copy())
    return data
"""

#---------------------------------------------

def genericTranslateInDict(cursor):
    """
    Translate a query cursor into a dictionari containing result row
    """
    
    data = {}
    key = []
    for row in cursor.description:
        key.append(row[0])

    jkey = 0
    for row in cursor.fetchall():
        i = 0
        dic = {}
        for val in row:
            dic[key[i]] = val
            i += 1
        data[jkey] = dic.copy()
        jkey += 1
    return data

#---------------------------------------------
"""
class Params:
    
    Class that contains the params submitted by the user
    and set the default values
    Used to submit arguments to the database connection methods
    

    def __init__(self, request):
        self.SiteName = request.GET.get('sitename', 'summary')
        self.TStart = request.GET.get('tstart', 
                                      datetime.strftime(date.today()-timedelta(days=7), 
                                      "%Y-%m-%d"))
        self.TStop = request.GET.get('tstop', 
                                     datetime.strftime(date.today(), 
                                     "%Y-%m-%d"))
        self.orderVar = request.GET.get('orderby', '')
        self.AggrFlag = request.GET.get('aggr', 'day')
        self.CollName = request.GET.get('collname', 'AOD')
        self.FirstN = int(request.GET.get('n', 3))
"""       
