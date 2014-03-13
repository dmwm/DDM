"""
"""


import logging

from dq2.common.DQLog import DQLog
from dq2.common.testcase.DQTestCase import DQTestCase


class TrapOperationsOnClosedFilesTestCase (DQTestCase):
    """
    @since: 0.3.0
    """


    def __init__ (self, name):
        """
        @since: 0.3.0
        
        @param name: the test name.
        @type name: str
        """
        DQTestCase.__init__(self, name)


    def setUp (self):
        """
        @since: 0.3.0
        
        this will force the following condition to happen.
        
        File "/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/logging/handlers.py", line 73, in emit
            if self.shouldRollover(record):
          File "/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/logging/handlers.py", line 147, in shouldRollover
            self.stream.seek(0, 2)  #due to non-posix-compliant Windows feature
        ValueError: I/O operation on closed file
        
        @see: http://docs.python.org/lib/module-logging.html
        """
        global LOG
        
        # setup the logger class
        LOG = DQLog('dq2.common')
        
        # inform the logging system to perform an orderly shutdown by flushing and closing all handlers.
        logging.shutdown()


    def tearDown (self):
        """
        @since: 0.3.0
        """
        pass


    def testShouldTrapOperationOnClosedFiles (self):
        """
        @since: 0.3.0
        
        1. test it traps errors when trying to write into a closed log file.
        """
        try:
            LOG.debug('Hello World!')
        except ValueError, e:
            fail(e)


if __name__ == '__main__':
    """
    Runs all tests in TrapOperationsOnClosedFilesTestCase.
    
    @since: 0.2.0
    """
    import sys
    test = TrapOperationsOnClosedFilesTestCase.main(
        'dq2.common.testcase', TrapOperationsOnClosedFilesTestCase.__name__, sys.argv[1:]
    )
    sys.exit(0)
