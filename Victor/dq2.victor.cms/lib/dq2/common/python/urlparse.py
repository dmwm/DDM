"""
On py2.3 urlparse doesn't have the same behaviour.

@see: http://www.python.org/doc/2.5/lib/module-urlparse.html
@see: http://www.python.org/doc/2.3.5/lib/module-urlparse.html

@since: 1.0.0
@version: $Id: urlparse.py,v 1.4 2010-10-04 13:24:10 vgaronne Exp $
"""


import httplib
import sys
import urlparse


class Url (tuple):
    """
    @author: Pedro Salgado
    @contact: pedro.salgado@cern.ch
    @since: 1.0.0
    @version: $Id: urlparse.py,v 1.4 2010-10-04 13:24:10 vgaronne Exp $
    
    @ivar scheme: URL scheme specifier.
    @type scheme: str
    @ivar netloc: the network location part.
    @type netloc: str
    @ivar path: the hierarchical path.
    @type path: str
    @ivar params: parameters for last path element.
    @type params: str
    @ivar query: the query component.
    @type query: str
    @ivar fragment: the fragment identifier.
    @type fragment: str
    @ivar hostname: the name of the host.
    @type hostname: str
    @ivar username: the user name.
    @type username: str
    @ivar password: the password.
    @type password: str
    @ivar port: the port of the host.
    @type port: int
    """
    def __init__ (self, tpl):
        """
        @param scheme: URL scheme specifier.
        @type scheme: str
        @param netloc: the network location part.
        @type netloc: str
        @param path: the hierarchical path.
        @type path: str
        @param params: parameters for last path element.
        @type params: str
        @param query: the query component.
        @type query: str
        @param fragment: the fragment identifier.
        @type fragment: str
        """
        super(tuple, self).__init__(tpl)
        
        self.tpl = tpl
        self.scheme = self.tpl[0]
        self.netloc = self.tpl[1]
        self.path = self.tpl[2]
        self.params = self.tpl[3]
        self.query = self.tpl[4]
        self.fragment = self.tpl[5]
        self.username = None
        self.password = None
        self.hostname = self.netloc[:self.netloc.find(':')]
        try:
            self.port = int(self.netloc[self.netloc.find(':')+1:])
        except ValueError as e:
            self.port = 80 # default port
        self.url = self.scheme +'://'+ self.netloc + self.path + '?' + self.query
    def __getattr__ (self, attrName):
        """"""
        if attrName == 'scheme':
            return self.tpl[0]
        elif attrName == 'netloc':
            return self.tpl[1]
        elif attrName == 'path':
            return self.tpl[2]
        elif attrName == 'params':
            return self.tpl[3]
        elif attrName == 'query':
            return self.tpl[4]
        elif attrName == 'fragment':
            return self.tpl[5]
        elif attrName == 'username':
            return None
        elif attrName == 'password':
            return None
        elif attrName == 'hostname':
            return self.hostname
        elif attrName == 'port':
            return self.port
        elif attrName == 'url':
            return self.url
    def geturl (self):
        return '%s://%s/%s?%s' % (self.scheme, self.netloc, self.path, self.query)
    def __str__ (self):
        """
        @return: the url information.
        @rtype: tuple (protocol, host:port, path, params, query string, fragment)
        """
        return str((self.scheme, self.netloc, self.path, self.params, self.query, self.fragment))
def urlparse (url, scheme='', allow_fragments=True):
    """
    This method is to override the python2.3 urlparse implementation
    and fake a python2.5 one.
    
    @see: http://svn.python.org/view/python/trunk/Lib/urlparse.py?rev=66196&view=auto
    
    Parse a URL into 6 components:
    <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
    Return a 6-tuple: (scheme, netloc, path, params, query, fragment).
    Note that we don't break the components up in smaller bits
    (e.g. netloc is a single string) and we don't expand % escapes.
    """
    tuple = urlparse.urlsplit(url, scheme, allow_fragments)
    scheme, netloc, url, query, fragment = tuple
    if scheme in uses_params and ';' in url:
        url, params = urlparse._splitparams(url)
    else:
        params = ''
    return Url((scheme, netloc, url, params, query, fragment))