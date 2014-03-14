"""
Script to run all tests for the dq2-common package.

@author: Pedro Salgado
@contact: pedro.salgado@cern.ch
@since: 0.4.0
@version: $Id: run.py,v 1.5 2010-10-12 08:07:10 vgaronne Exp $
"""

from dq2.common.testcase.DQLogTestSuite import DQLogTestSuite
from dq2.common.testcase.DQPingTestCase import DQPingTestCase
from dq2.common.testcase.UUIDTestCase import UUIDTestCase


def main ():
    """
    Run all tests for the dq2-common package.
    
    @since: 0.4.0
    """
    
    import unittest
    suite = DQLogTestSuite()
    suite.addTest(unittest.makeSuite(DQPingTestCase))
    suite.addTest(unittest.makeSuite(UUIDTestCase))
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    """
    @since: 0.4.0
    """
    main()