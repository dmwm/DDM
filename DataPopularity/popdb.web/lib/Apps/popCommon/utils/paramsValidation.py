from collections import defaultdict
from django.http import HttpResponse
from datetime import datetime, date, timedelta
import re

from Apps.popCommon.database import popCommonDB


class ParamValidationException(Exception):
    def __init__(self, param, cause):
        self.param = param
        self.cause = cause
    def __str__(self):
        return 'Error occurred during %s validation, cause: %s' % (self.param, self.cause)


def validateDate(input_date):
    try:
        in_date = datetime.strptime(input_date, "%Y-%m-%d")
        return True
    except Exception:
        return False

def validateSite(sitename):
    #return re.match(r'^T[0-9]_[A-Z]+_[a-z,A-Z]+|summary$', sitename) != None
    sitelist = popCommonDB.getSitesList()
    sitelist.append("summary")
    return sitename in sitelist

def validateDataTier(datatier):
    dtlist = popCommonDB.getDataTierList()
    return datatier in dtlist

def validateAggregation(aggr):
    valid_values = ['day', 'week', 'month', 'quarter', 'year']
    return aggr in valid_values

def validateOrder(order):
    valid_values = ['nacc', 'totcpu']
    return order in valid_values

def validateN(n):
    if n.isdigit():
        return int(n)>=0
    else:
        return False

class Params:

    """
    def __init__(self, request):
        self.SiteName = request.GET.get('sitename','summary')
        self.TStart   = request.GET.get('tstart',datetime.strftime(date.today()-timedelta(days=7),"%Y-%m-%d"))
        self.TStop    = request.GET.get('tstop',datetime.strftime(date.today(),"%Y-%m-%d"))
        self.orderVar = request.GET.get('orderby','')
        self.AggrFlag = request.GET.get('aggr','day')
        self.CollName = request.GET.get('collname','AOD')
        self.FirstN = int(request.GET.get('n',3))
    
    def validateDate(self, input_date):
        try:
            in_date = datetime.strptime(input_date, "%Y-%m-%d")
            return True
        except Exception:
            return False


    def validateAggregation(self, aggr):
        #valid_values = ['day', 'week', 'month', 'quarter', 'year']
        return aggr in self.aggregation_values

    def validateOrder(self, order):
        #valid_values = ['nacc', 'totcpu']
        return order in self.order_values

    def validateN(self, n):
        if n.isdigit():
            return int(n)>=0
        else:
            return False

    """

    def setSiteName(self, sitename):
        if validateSite(sitename):
            self.SiteName = sitename
        else:
            raise ParamValidationException('sitename', 'param must be a valid site name')


    def setTStart(self, tstart):
        if validateDate(tstart):
            self.TStart = tstart
        else:
            raise ParamValidationException('tstart', 'param must be a date')

    def setTStop(self, tstop):
        if validateDate(tstop):
            self.TStop = tstop
        else: 
            raise ParamValidationException('tstop', 'param must be a date')

    def setN(self, n):
        if validateN(n):
            self.FirstN = int(n)
        else:
            raise ParamValidationException('n', 'param must be a positive int')            

    def setAggregation(self, aggr):
        if validateAggregation(aggr):
            self.AggrFlag = aggr
        else:
            raise ParamValidationException('aggr', 'param must be a string in %s' % (self.aggregation_values))

    def setOrder(self, order):
        if validateOrder(order):
            self.orderVar = order
        else:
            raise ParamValidationException('orderby', 'param must be a string in %s' % (self.order_values))

class userStatParams(Params):

    def setCollName(self, collname):
        if validateDataTier(collname):
            self.CollName = collname
        else:
            raise ParamValidationException('CollName', 'param must be a valid dataset')
