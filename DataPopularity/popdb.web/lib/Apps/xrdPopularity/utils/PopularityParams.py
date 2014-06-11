import exceptions
from Apps.popCommon.database import popCommonDB
from Apps.popCommon.utils import Lexicon as lexicon
from Apps.popCommon.PopularityException import PopularityException, Paramvalidationexception
import logging
"""
class Paramvalidationexception(PopularityException):
    def __init__(self, param, cause):
        self.param = param
        self.cause = cause
        PopularityException.__init__(self, 'Error occurred during %s validation, cause: %s' % (self.param, self.cause))

    #def __str__(self):
    #    return 'Error occurred during %s validation, cause: %s' % (self.param, self.cause)
"""
logger = logging.getLogger(__name__)

DBUSER = 'CMS_EOS_POPULARITY_SYSTEM'

class Popularityparams():

    aggregationvalues = ['day', 'week', 'month', 'quarter', 'year']
    ordervalues = ['naccess', 'totcpu', 'nusers'] 
 
    def validatedate(self, inputdate):
        if lexicon.datestr(inputdate):
            return True
        raise Paramvalidationexception('inputdate', 'param must be a valid date')
    
    def validatedataset(self, dataset):
        if lexicon.dataset(dataset):
            dslist = popCommonDB.getDataSetList(DBUSER)
            dslist = map(lambda x: x["COLLNAME"], dslist)
            if dataset in dslist:
                return True
        raise Paramvalidationexception('dataset', 'param must be a valid dataset name')        

    def validateprocesseddataset(self, procdataset):
        if lexicon.processeddataset(procdataset):
            dslist = popCommonDB.getProcessedDataSetList(DBUSER)
            dslist = map(lambda x: x["COLLNAME"], dslist)
            if procdataset in dslist:
                return True
        raise Paramvalidationexception('processeddataset', 'param must be a valid processed dataset name')


    def validatesite(self, sitename):
        if lexicon.anstr(sitename) & (sitename == 'summary'):
            return True
        if lexicon.tier(sitename):
            sitelist = popCommonDB.getSitesList(DBUSER)
            if sitename in sitelist:
                return True
        raise Paramvalidationexception('sitename', 'param must be a valid site name')
	
    def validatedatatier(self, datatier):
        if lexicon.datatier(datatier):
            dtlist = popCommonDB.getDataTierList(DBUSER)
            dtlist = map(lambda x: x["COLLNAME"], dtlist)
            dtlist.append('ALL')
            if datatier in dtlist:
                return True
        raise Paramvalidationexception('datatier', 'param must be a valid datatier name')

    def validateaggregation(self, aggr):
        if lexicon.anstr(aggr) & (aggr in self.aggregationvalues):
            return True
        raise Paramvalidationexception('aggr', 'param must be value in %s' % self.aggregationvalues)
	
    def validateorder(self, order):
        if lexicon.anstr(order) & (order in self.ordervalues):
            return True
        raise Paramvalidationexception('order', 'param must be a value in %s' % self.ordervalues)
	    	
    def validaten(self, n):
        if n.isdigit():
            return True
        raise Paramvalidationexception('n', 'param must be a positive int')
	    
	    

    def setSiteName(self, sitename):
         
        if self.validatesite(sitename):
            self.SiteName = sitename
    
    def setDataSet(self, dataset):
        logger.info("in setdataset")
        if self.validatedataset(dataset):
            self.collName = dataset    

    def setProcessedDataSet(self, procdataset):
        logger.info("in setprocesseddataset")
        if self.validateprocesseddataset(procdataset):
            self.collName = procdataset



    def setTStart(self, tstart):
        if self.validatedate(tstart):
            self.TStart = tstart
        #else:
        #    raise Paramvalidationexception('tstart', 'param must be a date')

    def setTStop(self, tstop):
        if self.validatedate(tstop):
            self.TStop = tstop
        #else:
        #    raise Paramvalidationexception('tstop', 'param must be a date')

    def setN(self, n):
        if self.validaten(n):
            self.FirstN = int(n)
        #else:
        #    raise Paramvalidationexception('n', 'param must be a positive int')

    def setIsCentralUser(self,n):
        if ( n == '0' or n == '1' ):
            self.isUserCMS = int(n)
        else:
            raise Paramvalidationexception('centraluser', 'param must be 0 or 1')            


    def setAggregation(self, aggr):
        if self.validateaggregation(aggr):
            self.AggrFlag = aggr
        #else:
        #    raise Paramvalidationexception('aggr', 'param must be a string in %s' % (self.aggregationvalues))

    def setOrder(self, order):
        if self.validateorder(order):
            self.orderVar = order
        #else:
        #    raise Paramvalidationexception('orderby', 'param must be a string in %s' % (self.ordervalues))
            
            
class Userstatparams(Popularityparams):

    def setCollName(self, collname):
        if Popularityparams.validatedatatier(self, collname):
            self.collName = collname
        #else:
        #    raise Paramvalidationexception('CollName', 'param must be a valid dataset')
                                         
