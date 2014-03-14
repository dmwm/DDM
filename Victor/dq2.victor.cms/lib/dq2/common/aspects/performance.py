"""
Performance measurement aspect.

@author: Pedro Salgado
@contact: pedro.salgado@cern.ch
@since: 0.3.0
@version: $Id: performance.py,v 1.8 2008-06-17 17:10:02 psalgado Exp $
"""

import time

LOG = None


def get_logger ():
    """
    Returns a DQLog instance.
    
    @since: 0.3.0
    """
    global LOG
    
    if LOG is not None:
        return LOG
    
    from dq2.common.DQLog import DQLog
    return DQLog('dq2.common')


LOG = get_logger()


def performance (self, *args, **kwargs):
    """
    @since: 0.3.0
    """
    
    measure_start = time.time()
    try:
        return self.__proceed(*args, **kwargs)
    finally:
        measure_stop = time.time()
        
        # do nothing with this info for now!
        
        component = self.__class__.__name__ + '.' + str(self.__proceed_stack[-1].method.__name__)
        
        LOG.performance(
            '%s' % (measure_stop - measure_start),
            tuid=self.tuid,
            component=component
        )