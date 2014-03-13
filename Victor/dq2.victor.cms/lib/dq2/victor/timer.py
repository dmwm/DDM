"""
@copyright: European Organization for Nuclear Research (CERN)
@author: Fernando H. Barreiro U{fernando.harald.barreiro.megino@cern.ch<mailto:fernando.harald.barreiro.megino@cern.ch>}, CERN, 2012
@license: Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at U{http://www.apache.org/licenses/LICENSE-2.0}
"""

from dq2.common import log as logging

from functools import wraps
from time import time

def timed(f):
  @wraps(f)
  def wrapper(*args, **kwds):
    start = time()
    result = f(*args, **kwds)
    elapsed = time() - start
    print "%s took %d time to finish" % (f.__name__, elapsed)
    return result
  return wrapper

class Timer:
    """
    Class with Borg design pattern:
    http://code.activestate.com/recipes/66531-singleton-we-dont-need-no-stinkin-singleton-the-bo/
    The dictionary 
    """
    __timings = {'accounting' : {'calls': 0, 'time': 0},
                 'deletedVol' : {'calls': 0, 'time': 0},
                 'refreshAcc' : {'calls': 0, 'time': 0}, 
                 'popularity' : {'calls': 0, 'time': 0},
                 'setMetadata': {'calls': 0, 'time': 0},
                 'thresholds' : {'calls': 0, 'time': 0}
                }
    
    __logger = logging.getLogger("dq2.victor.timer")

    
    def __init__(self):
        self.__dict__ = self.__shared_state


    def increaseAccounting(self, time):
        self.__timings['accounting']['calls'] += 1
        self.__timings['accounting']['time']  += time


    def increaseDeletedVolume(self, time):
        self.__timings['deletedVol']['calls'] += 1
        self.__timings['deletedVol']['time']  += time


    def increasePopularity(self, time):
        self.__timings['popularity']['calls'] += 1
        self.__timings['popularity']['time']  += time


    def increaseSetMetadata(self, time):
        self.__timings['setMetadata']['calls'] += 1
        self.__timings['setMetadata']['time']  += time


    def increaseThresholds(self, time):
        self.__timings['thresholds']['calls'] += 1
        self.__timings['thresholds']['time']  += time
      
    def printout(self):
        self.__logger.info("""
                           Accounting  calls: %d in %.1f
                           DeletedVol  calls: %d in %.1f
                           RefreshAcc  calls: %d in %.1f                           
                           Popularity  calls: %d in %.1f
                           setMetadata calls: %d in %.1f
                           Thresholds  calls: %d in %.1f
                           """%(self.__timings['accounting']['calls'],  self.__timings['accounting']['time'],
                                self.__timings['deletedVol']['calls'],  self.__timings['deletedVol']['time'],
                                self.__timings['refreshAcc']['calls'],  self.__timings['refreshAcc']['time'],
                                self.__timings['popularity']['calls'],  self.__timings['popularity']['time'],
                                self.__timings['setMetadata']['calls'], self.__timings['setMetadata']['time'],
                                self.__timings['thresholds']['calls'],  self.__timings['thresholds']['time']))
