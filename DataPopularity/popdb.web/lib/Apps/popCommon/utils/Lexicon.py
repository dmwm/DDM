"""
_Lexicon_

A set of regular expressions  and other tests that we can use to validate input
to other classes. If a test fails an AssertionError should be raised, and
handled appropriately by the client methods, on success returns True.
"""

import re
import string
from datetime import datetime

class LexiconException(Exception):
    def __init__(self, candidate, regexpr):
        self.candidate = candidate
        self.regexpr = regexpr
    def __str__(self):
        return "'%s' does not match regular expression %s" % (candidate, regexp)


hostname = "(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])"
dateformat = "%Y-%m-%d"

def check(regexp, candidate):
    """
    assert re.compile(regexp).match(candidate) != None , \
    "'%s' does not match regular expression %s" % (candidate, regexp)
    return True
    """
    if re.compile(regexp).match(candidate) != None:
        return True
    else:
        #raise LexiconException(candidate, regexp)
        return False

def anstr(candidate):    
    return check(r'^[a-zA-Z0-9][a-zA-Z0-9]*$', candidate)
   
def datatier(candidate):
    return check(r'^[a-zA-Z0-9][a-zA-Z0-9-\-]*$', candidate) 
   
def processeddataset(candidate):
    return check(r'^[a-zA-Z0-9][a-zA-Z0-9\-\_]*$', candidate)

def dataset(candidate):
    return check( r'^/[a-zA-Z0-9\-\_]+/[a-zA-Z0-9\-\_]+/[a-zA-Z0-9\-\_]+', candidate)
 
def tier(candidate):
    return check("^T[0-9]_[A-Z]+_[A-Za-z0-9]+(_[A-Za-z0-9]*)?$", candidate)
    
def wildcardtier(candidate):
    #if re.compile("%").match(candidate) != None:
    if "%" in candidate:
        candidate = candidate.rstrip('%')
        return check("^T(([0-3](_[A-Z]*(_[A-Za-z0-9]*){1,2})?)?)$", candidate)
    else:
        return tier(candidate)

def hostname(candidate):
    #regexpression = "^http[s]?://%s$" % (hostname)
    regexpression = "^http[s]?://(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$"
    return check(regexpression, candidate)
    
def datestr(candidate):
    try:
        candidatetodate = datetime.strptime(candidate, dateformat)
        return True
    except Exception:
        #raise LexiconException(candidate, dateformat)
        return False

def accsource(candidate):
    return candidate == 'crab' or candidate == 'xrootd'    
