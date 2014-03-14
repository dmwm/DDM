"""
@author: Pedro Salgado
@contact: pedro.salgado@cern.ch
@since: 1.0
@version: $Id: exceptions.py,v 1.14 2010-10-04 13:24:09 vgaronne Exp $
"""

from dq2.common.DQException import DQException, DQFatalError, DQNonFatalError, DQSecurityException, DQUserError

from dq2.common.constants import DatasetState


#
# FILE
#


class DQUnknownFileException (DQException, DQUserError, DQNonFatalError):
    """
    DQException class for the cases when a expected file isn't found.
    
    @author: Pedro Salgado
    @contact: pedro.salgado@cern.ch
    @since: 1.0
    @version: $Revision: 1.14 $
    """
    def __init__ (self, lfn, root_cause=None):
        """
        
        
        @since: 1.0
        
        @param lfn: the logical file name.
        @type lfn: str
        """
        self.lfn = lfn
        DQException.__init__(self, root_cause=root_cause)
    def __str__(self):
        """
        Returns a string representation of this object.
        
        @since: 1.0
        """
        message = 'Unknown file %s !' % (self.lfn)
        return '%s%s %s' % (DQUserError.prefix, DQNonFatalError.prefix, message)