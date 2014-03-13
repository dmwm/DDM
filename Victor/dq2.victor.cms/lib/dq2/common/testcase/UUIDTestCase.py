"""
@author: Pedro Salgado
@contact: pedro.salgado@cern.ch
@since: 0.4.0
@version: $Id: UUIDTestCase.py,v 1.4 2010-10-12 08:07:10 vgaronne Exp $
"""


import logging


from dq2.common import generate_uuid
from dq2.common.DQLog import DQLog
from dq2.common.testcase.DQTestCase import DQTestCase
from dq2.common.validator.DQValidator import is_uid


class UUIDTestCase (DQTestCase):
    """
    @since: 0.4.0
    """


    def __init__ (self, name):
        """
        @since: 0.3.0
        
        @param name: the test name.
        @type name: str
        """
        DQTestCase.__init__(self, name)


    def test (self):
        """
        @since: 0.4.0
        
        1. test it traps errors when trying to write into a closed log file.
        """        
        is_uid([generate_uuid()])


if __name__ == '__main__':
    """
    Runs all tests in UUIDTestCase.
    
    @since: 0.2.0
    """
    import sys
    test = UUIDTestCase.main(
        'dq2.common.testcase', UUIDTestCase.__name__, sys.argv[1:]
    )
    sys.exit(0)