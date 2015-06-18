"""
Exception handling aspect.

@author: Pedro Salgado
@contact: pedro.salgado@cern.ch
@since: 0.3.0
@version: $Id: exception.py,v 1.6 2008-06-17 17:10:02 psalgado Exp $
"""


def wrap_package ():
    """
    Loads the exception handling aspect for the dq2.common package.
    
    @since: 0.3.0
    """
    
    from dq2.common.aspects import wrap_around
    from dq2.common.DQLog import DQLog
    
    wrap_around(DQLog.debug, wrap_message)
    wrap_around(DQLog.error, wrap_message)
    wrap_around(DQLog.info, wrap_message)
    wrap_around(DQLog.performance, wrap_message)
    wrap_around(DQLog.trace, wrap_message)


def wrap_message (self, message, tuid='', component=''):
    """
    This method is used to wrap logging errors and prevent them to crash the central catalogs.
    
    @bug: 27575 DQ2 0.3.0: python logging ValueError: I/O operation on closed file.
    @see: https://savannah.cern.ch/bugs/?27575
    
    @param message: the message to be logged.
    @type message: str
    @keyword tuid: the transaction unique identifier.
    @type tuid: str
    @keyword component: the software component.
    @type component: str
    """
    try:
        return self.__proceed(message, tuid=tuid, component=component)
    except StandardError as e:
        """don't stop the application because of a logging error."""
        pass