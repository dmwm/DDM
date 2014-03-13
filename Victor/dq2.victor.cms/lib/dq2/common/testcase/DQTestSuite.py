"""
DQ test suite.

@author: Pedro Salgado
@contact: pedro.salgado@cern.ch
@since: 0.3.0
@version: $Id: DQTestSuite.py,v 1.10 2010-10-12 08:07:10 vgaronne Exp $
"""

from unittest import TestSuite


class DQTestSuite (TestSuite):
    """
    @since: 0.3.0
    @version: $Revision: 1.10 $
    """


    def __init__ (self, testcases):
        """
        Constructs a DQTestSuite instance.
        
        @since: 0.3.0
        
        @param testcases: testcases to run.
        @type testcases: list
        
        @warning:
            you have to always explicitely delete the test suite object [del(suite)],
            when using Oracle instances,
            so that the database pool monitoring thread is stopped.
        """
        TestSuite.__init__(self)
        
        for eachTestCase in testcases:
            for method in dir(eachTestCase):
                lmethod = method.lower()
                if lmethod.startswith('test') or \
                    lmethod.startswith('alternative') or \
                    lmethod.startswith('scenario') or \
                    lmethod.startswith('attempt'):
                    """method name starts by 'test': add it to the test suite"""
                    self.addTest(eachTestCase(method))
