"""
@author: Pedro Salgado
@contact: pedro.salgado@cern.ch
@since: 0.2.0
@version: $Id: DQException.py,v 1.13 2010-10-04 13:24:10 vgaronne Exp $
"""


import string


class DQException: # (Exception):
    """
    Base exception class.
    
    @since: 0.2.0
    @version: $Revision: 1.13 $
    
    @cvar __version__: the class version.
    @type __version__: str
    """


    __version__ = '$Revision: 1.13 $'


    def __init__ (self, root_cause=None):
        """
        
        @since: 0.2.0
        @version: $Revision: 1.13 $
        
        @ivar root_cause: the original error/exception.
        @type root_cause: object
        @ivar tuid: the transaction unique identifier.
        @type tuid: st
        @deprecated: tuid will be deprecated in DQ2 1.0
        """
        self.root_cause = root_cause
        self.tuid = None


    def __repr__ (self):
        """
        Returns the cPickle representation of this object.
        
        @since: 0.2.0
        
        @return: this object pickled
        @rtype: str
        """
        import cPickle        
        try:
            return cPickle.dumps(self)            
        except cPickle.PicklingError as e:
            return str(self)
        


    def __help__ (self):
        """
        @since: 0.3.0
        """
        return """
    root_cause : %s
        """ % (str(self.root_cause))


    def _escape_arguments(self, argument):
        """
        @since: 0.3
        """
        return str(argument).replace("'", '"').replace('\n', '')


class DQBackendException (DQException):
    """
    @since: 0.2.0
    
    @ivar desc: exception error message.
    @type desc: str
    """


    def __init__ (self, desc):
        """
        Constructs a DQBackendException instance.
        
        @since: 0.2
        @version: $Revision: 1.13 $
        """
        self.desc = desc
        DQException.__init__(self)


    def __str__(self):
        """
        Returns a string representation of this object.
        
        @since: 0.2.0
        
        @return: string representation of this object.
        @rtype: str
        """
        return 'DQ2 backend exception [%s]' % (self.desc)


# KINDs of errors


class DQFatalError:
    """
    Class for unrecoverable errors.
    This kind of error stops the user request.
    
    @since: 0.3.1
    @version: $Revision: 1.13 $
    
    @cvar __version__: the class version.
    @type __version__: str
    @cvar prefix: prefix of this kind of error messages.
    @type prefix: str
    """
    __version__ = '$Revision: 1.13 $'
    prefix = '[FATAL]'

    def __init__ (self):
        """
        @since: 0.3.0
        """
        pass


class DQNonFatalError:
    """
    Class for recoverable errors.
    This kind of error stops the user request.
    
    @since: 0.3.1
    @version: $Revision: 1.13 $
    
    @cvar __version__: the class version.
    @type __version__: str
    @cvar prefix: prefix of this kind of error messages.
    @type prefix: str
    """
    __version__ = '$Revision: 1.13 $'
    prefix = '[OTHER]'

    def __init__ (self):
        """
        @since: 0.3.0
        """
        pass


class DQWarning:
    """
    Class for warnings.
    This kind of error *DOES NOT* stop the user request.
    
    @since: 0.3.1
    @version: $Revision: 1.13 $
    
    @cvar __version__: the class version.
    @type __version__: str
    @cvar prefix: prefix of this kind of error messages.
    @type prefix: str
    """
    __version__ = '$Revision: 1.13 $'
    prefix = '[WARNING]'

    def __init__ (self):
        """
        @since: 0.3.0
        """
        pass


# CLIENT-side exceptions


class DQUserError:
    """
    Class for user errors.
    
    @since: 0.3.1
    @version: $Revision: 1.13 $
    
    @cvar __version__: the class version.
    @type __version__: str
    @cvar prefix: prefix of this kind of error messages.
    @type prefix: str
    """
    __version__ = '$Revision: 1.13 $'
    prefix = '[USER]'

    def __init__ (self):
        """
        @since: 0.3.0
        """
        pass


class DQConfigurationException (DQException, DQUserError, DQWarning):
    """
    @since: 0.3.1
    @version: $Revision: 1.13 $
    """


    def __init__ (self, desc, root_cause=None):
        """
        Constructs a DQConfigurationException instance.
        
        @param desc: .
        @type desc: str
        @param root_cause: .
        @type root_cause: Exception
        """
        self.desc = desc
        DQException.__init__ (self, root_cause=root_cause)


    def __str__ (self):
        """
        Returns a string representation of this object.
        
        @since: 0.3.1
        """
        return '%s%s %s' % (DQUserError.prefix, DQWarning.prefix, self.desc)


class DQInvalidRequestException (DQException, DQUserError, DQNonFatalError):
    """
    @since: 0.2.0
    @version: $Revision: 1.13 $
    """


    def __init__ (self, message):
        """
        Constructs a DQInvalidRequestException instance.
        
        @param message: error message.
        @type message: str
        """
        self.message = message
        DQException.__init__ (self)


    def __str__ (self):
        """
        Returns a string representation of this object.
        
        @since: 0.2.0
        """
        return '%s%s %s' % (DQUserError.prefix, DQNonFatalError.prefix, self.message)


class DQSecurityException (DQException, DQUserError, DQNonFatalError):
    """
    @since: 0.2.0
    @version: $Revision: 1.13 $
    
    @ivar message: error message.
    @type message: str
    """


    def __init__ (self, message, root_cause=None):
        """
        Constructs a DQSecurityException instance.
        
        @param message: error message.
        @type message: str
        @param root_cause: .
        @type root_cause: Exception
        """
        self.message = message
        DQException.__init__ (self, root_cause=root_cause)


    def __str__ (self):
        """
        Returns a string representation of this object.
        
        @since: 0.2.0
        """
        return '%s%s %s' % (DQUserError.prefix, DQNonFatalError.prefix, self.message)


class DQCurlError:
    """
    Class for (py)curl errors.
    
    @since: 0.3.1
    @version: $Revision: 1.13 $
    
    @cvar __version__: the class version.
    @type __version__: str
    @cvar prefix: prefix of this kind of error messages.
    @type prefix: str
    """
    __version__ = '$Revision: 1.13 $'
    prefix = '[(py)CURL]'

    def __init__ (self):
        """
        @since: 0.3.0
        """
        pass


# SERVER-side exceptions


class DQWebServerError:
    """
    Class for web server errors.
    
    @since: 0.3.1
    @version: $Revision: 1.13 $
    
    @cvar __version__: the class version.
    @type __version__: str
    @cvar prefix: prefix of this kind of error messages.
    @type prefix: str
    """
    __version__ = '$Revision: 1.13 $'
    prefix = '[WEBSERVER]'

    def __init__ (self):
        """
        @since: 0.3.0
        """
        pass


class DQBadServerResponse (DQException, DQWebServerError, DQFatalError):
    """
    Exception class for bad web server responses.
    
    @since: 0.3.0
    @version: $Revision: 1.13 $
    """


    def __init__ (self, response, url, urlsec, curl_error):
        """
        Constructs a DQBadServerResponse instance.
        
        @param response: web server response.
        @type response: str
        @param url: .
        @type url: str
        @param urlsec: .
        @type urlsec: str
        @param curl_error: curl error message.
        @type curl_error: str
        """
        self.response = response
        self.url = url
        self.urlsec = urlsec
        self.curl_error = curl_error


    def __str__(self):
        """
        Returns a string representation of this object.
        
        @since: 0.3.0
        """
        message = 'The server returned a bad response!\n%s\n%s]\n[%s][%s]' % (self.url, self.urlsec, self.curl_error, self.response)
        return '%s%s %s' % (DQWebServerError.prefix, DQFatalError.prefix, message)


class DQWebServiceError:
    """
    Class for web service errors.
    
    @since: 0.3.1
    @version: $Revision: 1.13 $
    
    @cvar __version__: the class version.
    @type __version__: str
    @cvar prefix: prefix of this kind of error messages.
    @type prefix: str
    """
    __version__ = '$Revision: 1.13 $'
    prefix = '[WEBSERVICE]'

    def __init__ (self):
        """
        @since: 0.3.0
        """
        pass


class DQDNBlockedException (DQException, DQWebServiceError, DQFatalError):
    """
    Exception class for...
    
    @author: David Cameron
    @contact: david.cameron@cern.ch
    @since: 0.3.0
    @version: $Revision: 1.13 $
    
    @ivar dn: .
    @type dn: str
    """


    def __init__ (self, dn):
        """
        Constructs a DQDNBlockedException instance.
        
        @param dn: description.
        @type dn: str
        """
        self.dn = dn


    def __str__ (self):
        """
        Returns a string representation of this object.
        @since: 0.3.0
        """
        message = 'The DN ( %s ) is blocked!' % (self.dn)
        return '%s%s %s' % (DQWebServiceError.prefix, DQFatalError.prefix, message)


class DQInvalidAPIException (DQException, DQWebServiceError, DQFatalError):
    """
    @since: 0.3.0
    @version: $Revision: 1.13 $
    
    @ivar api: .
    @type api: str
    """


    def __init__ (self, api):
        """
        Constructs a DQInvalidAPIException instance.
        
        @param api: .
        @type api: str
        """
        self.api = api
        DQException.__init__(self, None)


    def __str__ (self):
        """
        Returns a string representation of this object.
        
        @since: 0.2.0
        """
        message = "%s isn't a valid API." % (self.api)
        return '%s%s %s' % (DQWebServiceError.prefix, DQFatalError.prefix, message)


class DQInvalidWebServiceOperationException (DQException, DQWebServiceError, DQFatalError):
    """
    Exception class for the cases where a HTTP call has an invalid operation parameter.
    
    @since: 0.3.0
    @version: $Revision: 1.13 $
    """


    def __init__ (self, root_cause=None):
        """
        Constructs a DQInvalidWebServiceOperationException instance.
        
        @param root_cause: .
        @type root_cause: Exception
        """
        DQException.__init__ (self, root_cause=root_cause)


    def __str__ (self):
        """
        Returns a string representation of this object.
        
        @since: 0.2.0
        """
        message = 'HTTP request has an invalid operation!'
        return '%s%s %s' % (DQWebServiceError.prefix, DQFatalError.prefix, message)


class DQInvalidWebServiceHeaderException (DQException, DQWebServiceError, DQFatalError):
    """
    Exception class for the cases where a HTTP call is missing parameters.
    
    @since: 0.3.0
    @version: $Revision: 1.13 $
    
    @ivar header: name of the header.
    @type header: str
    """


    def __init__ (self, header, root_cause=None):
        """
        Constructs a DQInvalidWebServiceHeaderException instance.
        
        @param header: name of the header.
        @type header: str
        @param root_cause: .
        @type root_cause: Exception
        """
        self.header = header
        DQException.__init__ (self, root_cause=root_cause)


    def __str__ (self):
        """
        Returns a string representation of this object.
        
        @since: 0.2.0
        """
        message = 'HTTP request is missing mandatory header (%s)!' % (self.header)
        return '%s%s %s' % (DQWebServiceError.prefix, DQFatalError.prefix, message)


class DQInvalidWebServiceParameterException (DQException, DQWebServiceError, DQFatalError):
    """
    Exception class for the cases where a HTTP call is missing parameters.
    
    @since: 0.3.0
    @version: $Revision: 1.13 $
    
    @ivar param: name of the parameter.
    @type param: str
    """


    def __init__ (self, param, root_cause=None):
        """
        Constructs a DQInvalidWebServiceParameterException instance.
        
        @param param: name of the parameter.
        @type param: str
        @param root_cause: .
        @type root_cause: Exception
        """
        self.param = param
        DQException.__init__(self, root_cause=root_cause)


    def __str__ (self):
        """
        Returns a string representation of this object.
        
        @since: 0.3.0
        """
        message = 'HTTP request is missing mandatory parameter (%s)!' % (self.param)
        return '%s%s %s' % (DQWebServiceError.prefix, DQFatalError.prefix, message)
