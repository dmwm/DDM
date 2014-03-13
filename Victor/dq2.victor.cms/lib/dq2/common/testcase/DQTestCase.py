"""
DQ testcase.

@author: Pedro Salgado
@contact: pedro.salgado@cern.ch
@since: 0.3.0
@version: $Id: DQTestCase.py,v 1.14 2010-10-12 08:07:10 vgaronne Exp $
"""


import commands
import string
import unittest


class DQTestCase (unittest.TestCase):
    """
    @since: 0.2.0
    @version: $Revision: 1.14 $
    """


    debugEnabled = False
    loadedDebug = False
    
    try:
        from dq2.common.client import x509
        
        user_cert = x509.get_x509()
        user_dn = x509.get_dn()
    except:
        user_cert = '/DC=ch/DC=cern/OU=Organic Units/OU=Users/CN=dq2/CN=000000'
        user_dn = '/DC=ch/DC=cern/OU=Organic Units/OU=Users/CN=dq2/CN=000000'


    def __init__ (self, name):
        """
        Constructs a DQTestCase instance.
        
        @since: 0.3.0
        
        @param name: test name.
        @type name: str
        """
        
        unittest.TestCase.__init__(self, name)
        
        if DQTestCase.debugEnabled and not DQTestCase.loadedDebug:
            import sys
            from dq2.common.testcase import traceit
            sys.settrace(traceit)
            DQTestCase.debugEnabled = True
            DQTestCase.loadedDebug = True # to guarantee the import is done only once
        
        self.certificate = DQTestCase.user_dn


# PRIVATE methods


    def _find_error (self, expected, result):
        """
        @since: 0.3.0
        """
        error = ''
        
        if isinstance(expected, dict) and isinstance(result, dict):
            iterator = None
            if len(expected.keys()) >= len(result.keys()):
                iterator = expected.keys()
            else:
                iterator = result.keys()
            
            for eachKey in iterator:
                if not result.has_key(eachKey) or not expected.has_key(eachKey):
                    """error is missing key on result"""
                    error += " missing key '%s' on the result dictionary\n" % (str(eachKey))
                elif not expected[eachKey] == result[eachKey]:
                    """error is value mismatch"""
                    if isinstance(expected[eachKey], dict) and isinstance(result[eachKey], dict):
                        error += " error in key '%s'\n" % (eachKey)
                        error += self._find_error(expected[eachKey], result[eachKey])
                    else:
                        error += " values for don't match \n\t%s\n\t%s\n" % (
                            str(expected[eachKey]), str(result[eachKey])
                        )
        return error


    def _fmt_message (self, case, expected, result=''):
        """
        Formats the testcase failure message.
        
        @since: 0.2.0
        
        @param case: name of the test.
        @type case: str
        @param expected: expected test result.
        @type expected: any
        @param result: test result.
        @type result: any
        
        @return: failure message (case, expected output and actual result).
        @rtype: str
        """
        error = self._find_error(expected, result)
        
        return """
%s
  E : '%s' (%s)
  R : '%s' (%s)
  
  ERROR:\n%s
""" % (str(case), str(expected), type(expected), str(result), type(result), str(error))


# PUBLIC methods


    def main (testClassModule, testClassName, args, debug=False):
        """
        Runs all tests in ...
        
        @since: 0.3.0
        
        @param testClassModule: module name.
        @type testClassModule: module
        @param testClassName: class name.
        @type testClassName: str
        @param args: tests to be performed.
        @type args: list
        @param debug: flag for debug option.
        @type debug: bool
        """
        
        import unittest
        code = 'from %s.%s import %s' % (testClassModule, testClassName, testClassName)
        exec(code)
        
        if len(args) >= 1:
            suite = unittest.TestSuite()
            for eachTest in args:
                code = 'suite.addTest(%s(eachTest))' % (testClassName)
                exec(code)
        
        else:
            code = 'unittest.makeSuite(%s)' % (testClassName)
            suite = eval(code)
        
        unittest.TextTestRunner(verbosity=2).run(suite)

    main = staticmethod(main)


    def setAnotherCertificate (self, other):
        """
        @since: 1.0
        
        @warning: this is only for client testing.
        """
        self.certificate = other