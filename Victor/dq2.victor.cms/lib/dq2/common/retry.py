from dq2.common.exceptions import *
from dq2.repository.DQRepositoryException import *
from time import sleep
from math import exp

import sys, traceback

def retry(func, *args, **kwargs):
    _min_sleep  = 0.001
    _max_sleep  = 900
    _multiplier = 2    
    _delay      = _min_sleep / _multiplier
    _attempt    =  0
    _max_attempt = 100 
    while True:
        try:
            return apply(func,args, kwargs)
        except Exception as e:
            print e
        except DQUnknownDatasetException as e:
            raise (e)            
        except DQFatalError as e:
            raise (e)        
        except:
            errno, errstr = sys.exc_info()[:2]
            print "%s failed with: %s, retry after delay %s "%(str(func), errstr, exp(_delay))
            sleep (exp(_delay))
            _delay = min(_delay * _multiplier, _max_sleep)
        if  _attempt ==  _max_attempt:
            raise 'Max attempt(%s) reached for %s %s %s'% (_attempt,str(func),str(args), str(kwargs))
        _attempt += 1