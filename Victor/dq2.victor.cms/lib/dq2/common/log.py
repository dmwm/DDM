"""
Contains the dashboard specific logging definitions.

In particular, it takes care of the logging configuration loading, looking in
the filesystem with the last one found having priority (overwriting previous 
values):
1) /opt/dq2/config/logging.cfg
2) $HOME/.dq2/config/logging.cfg
3) $DQ2_HOME/config/logging.cfg

@author: Ricardo Rocha
@contact: ricardo.rocha@cern.ch
@since: 0.3
@version: $Id: log.py,v 1.10 2010-10-04 13:24:09 vgaronne Exp $
"""

try:
    import ConfigParser
    import logging
    import logging.config
    
    from dq2.common        import WriteAllRotatingFileHandler
    from dq2.common.Config import Config
    
    """
    This has to be done before importing the classes where the logger objects
    are class members.
    """
    try:
        logging.custhandlers                         = WriteAllRotatingFileHandler
        logging.handlers.WriteAllRotatingFileHandler = WriteAllRotatingFileHandler.WriteAllRotatingFileHandler
        logging.config.fileConfig(Config().getConfig(None).get('dq2', 'logging.config.file'))
    except ConfigParser.NoSectionError as e:
        pass
    
    _logger = logging.getLogger('dq2.common.log')
except:
    pass


def getLogger (logger):
    """
    @since: 0.3
    
    @param logger: .
    @type logger: 
    
    @return: logger.
    @rtype: object?
    """
    try:
        loggerObj = logging.getLogger(logger)
        if not loggerObj:
            _logger.error("Failed to get logger '%s'!" % logger)
        return loggerObj
    except:
        # python 2.2 uses fake logging
        class FakeLogger:
            def info(self, *args):
                pass
            def debug(self, *args):
                pass
            def warning(self, *args):
                pass
            warn = warning
            def error(self, *args):
                pass
            def exception(self, *args):
                pass
            def critical(self, *args):
                pass
            def log(self, *args):
                pass
        return FakeLogger()


class DQLog:
    """
    A generic class for output logs.
    
    @since: 0.3.0
    @version: $Revision: 1.10 $
    """


    def __init__ (self, instance):
        """
        Constructs a DQLog instance.
        
        @since: 0.3.0
        
        @param instance: .
        @type instance: 
        """
        self._logger = logging.getLogger(instance)


# PUBLIC methods


    def debug (self, message, tuid='', component=''):
        """
        Write a debug level message.
        
        @since: 0.3.0
        
        @param message: .
        @type message: 
        @param tuid: .
        @type tuid: 
        @param component: .
        @type component: 
        """
        try:
            self._logger.debug('[%s] [%s] %s' % (tuid, component, message))
        except:
            """don't stop the application because of a logging error."""
            pass


    def error (self, message, tuid='', component=''):
        """
        Write an error message.
        
        @since: 0.3.0
        
        @param message: .
        @type message: 
        @param tuid: .
        @type tuid: 
        @param component: .
        @type component:
        """
        try:
            self._logger.error('[%s] [%s] %s' % (tuid, component, message.replace('\n', ' ')))
        except:
            """don't stop the application because of a logging error."""
            pass


    def info (self, message, tuid='', component=''):
        """
        Write an info level message.
        
        @since: 0.3.0
        
        @param message: .
        @type message: 
        @param tuid: .
        @type tuid: 
        @param component: .
        @type component:
        """
        try:
            self._logger.info('[%s] [%s] %s' % (tuid, component, message))
        except:
            """don't stop the application because of a logging error."""
            pass


    def performance (self, message, tuid='', component=''):
        """
        Write a performance message.
        
        @since: 0.3.0
        
        @param message: .
        @type message: 
        @param tuid: .
        @type tuid: 
        @param component: .
        @type component:
        """
        try:
            self._logger.info('PERFORMANCE [%s] [%s] %s' % (tuid, component, message))
        except:
            """don't stop the application because of a logging error."""
            pass


    def trace (self, message, tuid='', component=''):
        """
        Write a trace message.
        
        @since: 0.3.0
        
        @param message: .
        @type message: 
        @param tuid: .
        @type tuid: 
        @param component: .
        @type component:
        """
        try:
            self._logger.debug('TRACE [%s] [%s] %s' % (tuid, component, message))
        except:
            """don't stop the application because of a logging error."""
            pass


    def warning (self, message, tuid='', component=''):
        """
        Write a warning level message.
        
        @since: 1.0
        
        @param message: .
        @type message: 
        @param tuid: .
        @type tuid: 
        @param component: .
        @type component:
        """
        try:
            self._logger.warning('[%s] [%s] %s' % (tuid, component, message))
        except:
            """don't stop the application because of a logging error."""
            pass





