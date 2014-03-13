"""
@since: 1.1.13
@version: $Id: httplib.py,v 1.3 2010-10-04 13:24:10 vgaronne Exp $
"""


import httplib


# these constants are missing in httplib 2.3 (among others)
httplib.OK = 200
httplib.REQUEST_TIMEOUT = 408