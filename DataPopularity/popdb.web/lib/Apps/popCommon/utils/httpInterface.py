import pycurl
import urllib
import platform
import cStringIO
import json
import logging

from Apps.popCommon.utils import Lexicon
from Apps.popCommon.PopularityException import PopularityException

logger = logging.getLogger(__name__)

class PopularityHttpInterfaceException(PopularityException):
    def __init__(self, error):
        self.err = "%s" % error
        PopularityException.__init__(self, '%s' % error)

class httpInterface:

    def __init__(self, url):
        self.host = url
        self.resource = ''
        self.caller = pycurl.Curl()
        self.validateHostName(url)
        header = 'PopDB API/1.0 (CMS) %s/%s %s/%s (%s)' % (pycurl.__name__, pycurl.version_info()[1], platform.system(), platform.release(), platform.processor())
        self.caller.setopt(pycurl.HTTPHEADER, ['User-agent: %s' % header])
        #self.caller.setopt(self.caller.URL, url)
        self.caller.setopt(self.caller.VERBOSE, True)
        self.caller.setopt(self.caller.SSL_VERIFYPEER, 0)

    def set_resource(self, resource):
        #url = self.caller.getinfo(pycurl.EFFECTIVE_URL)
        self.resource = resource
        #self.caller.setopt(self.caller.URL, url + resource)

    def set_header(self, header):
        self.caller.setopt(pycurl.HTTPHEADER, [header])


    def get_data(self, params):
        buf = cStringIO.StringIO()
        #url = self.caller.getinfo(pycurl.EFFECTIVE_URL)
        self.caller.setopt(self.caller.URL, self.host + self.resource + '?' + urllib.urlencode(params))
        self.caller.setopt(self.caller.WRITEFUNCTION, buf.write)
        logger.info(self.caller.getinfo(pycurl.EFFECTIVE_URL))
        self.caller.perform()
        return buf.getvalue()

    def get_json_data(self, params):
        self.caller.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
        try:
            data = self.get_data(params)
            return json.loads(data)
        except ValueError, err:
            logger.error('Unable to decode JSON from %s' % self.caller.getinfo(pycurl.EFFECTIVE_URL))
            logger.error(data)
            raise err

    def validateHostName(self, hostname):
        #pat = re.compile('^http[s]*://[a-zA-Z0-9\-\.]+$')
        if  not Lexicon.hostname(hostname):
            raise PopularityHttpInterfaceException("Given hostname has not a valid format")


