import exceptions
from Apps.popCommon.database import popCommonDB
from Apps.popCommon.utils import Lexicon as lexicon
from Apps.popCommon.PopularityException import Paramvalidationexception

"""
class Paramvalidationexception(exceptions.Exception):
    def __init__(self, param, cause):
        Exception.__init__(self)
        self.param = param
        self.cause = cause

    def __str__(self):
        return 'Error occurred during %s validation, cause: %s' % (self.param, self.cause)
"""

class victorinterfaceparams:
    """
    def __init__(self, request):
        self.SiteName = request.GET.get('sitename', 'T%')
        self.TStart = request.GET.get('tstart',
                                      datetime.strftime(date.today()-timedelta(days=30),
                                      "%Y-%m-%d"))
        self.TStop = request.GET.get('tstop',
                                     datetime.strftime(date.today(),"%Y-%m-%d"))
    """

    def validatedate(self, inputdate):
        if lexicon.datestr(inputdate):
            return True
        raise Paramvalidationexception('inputdate', 'param must be a valid date')
                                 
    def validateSite(self, sitename):
        if (sitename == '') | (lexicon.wildcardtier(sitename)):
            return True
        raise Paramvalidationexception('sitename', 'param must be a valid site name')

    def validateSource(self, source):
        if lexicon.accsource(source):
             return True
        raise Paramvalidationexception('source', 'param must be a valid source name')

    def validateDir(self, dirname):
        if lexicon.dirname(dirname):
            return True
        raise Paramvalidationexception('dirname', 'param must be a valid directory name')

    """
    def validateSite(self, sitename):
        if sitename == '':
            return True
        elif lexicon.wildcardtier(sitename):
            return True
        else: 
            return False
    """

    """
    def setSiteName(self, sitename):
        if self.validateSite(sitename):
            self.SiteName = sitename
        else:
            raise Paramvalidationexception('sitename', 'param must be a valid site name')
    """

    def setSiteName(self, sitename):
        if self.validateSite(sitename):
            self.SiteName = sitename

    def setTStart(self, tstart):
        if self.validatedate(tstart):
            self.TStart = tstart
        #else:
        #    raise Paramvalidationexception('tstart', 'param must be a date')

    def setTStop(self, tstop):
        if self.validatedate(tstop):
            self.TStop = tstop

    def setSource(self, source):
        if self.validateSource(source):
            self.source = source

    def setTopDir(self, dirname):
        if self.validateDir(dirname):
            self.TopDir = dirname
