"""
Testcase to verify the DQLog behaviour.

@author: Pedro Salgado
@contact: pedro.salgado@cern.ch
@since: 0.3.0
@version: $Id: DQLogTestSuite.py,v 1.5 2010-10-12 08:07:10 vgaronne Exp $
"""


import logging

from dq2.common.DQLog import DQLog
from dq2.common.testcase.DQTestSuite import DQTestSuite
from dq2.common.testcase.TrapOperationsOnClosedFilesTestCase import TrapOperationsOnClosedFilesTestCase


class DQLogTestSuite (DQTestSuite):
    """
    @since: 0.3.0
    @version: $Revision: 1.5 $
    """


    def __init__ (self):
        """
        Constructs a DQLogTestSuite instance.
        
        @since: 0.3.0
        """
        self.suite = DQTestSuite.__init__(
            self,
            [
                TrapOperationsOnClosedFilesTestCase
            ]
        )


if __name__ == '__main__':
    """
    Runs all tests in DQLogTestSuite.
    
    @since: 0.3.0
    """
    import unittest
    suite = DQLogTestSuite()
    unittest.TextTestRunner(verbosity=2).run(suite)
