"""
Testcase for the dq2.common.DQPing module.

@author: Pedro Salgado
@contact: pedro.salgado@cern.ch
@since: 0.2
@version: $Id: DQPingTestCase.py,v 1.6 2010-10-12 08:07:10 vgaronne Exp $

@requires: python 2.4. in previous versions of Python the test on dq2.common.DQPing.pings will hang.
"""


import dq2.common.DQPing


from dq2.common.testcase.DQTestCase import DQTestCase


class DQPingTestCase (DQTestCase):
    """
    Testcase for the dq2.common.DQPing module.
    
    @since: 0.2.2
    """


    def __init__ (self, name=False):
        """
        Constructs an instance of DQPingTestCase.
        
        @since: 0.2.2
        
        @param name: testcase name.
        @type name: str
        """
        DQTestCase.__init__(self, name)
        
        self.ip_valid = '127.0.0.1'
        self.ip_unknown_host = '128.0.0.1'
        
        self.urls = [
            'http://www.cern.ch/',
            'http://www.cern.ch:8/',
            'http://www.cern.ch:80/',
            'http://www.cern.ch:800/',
            'http://www.cern.ch:8000/',
            'http://www.cern.ch:/',
            'http://www.cern.ch',
            'http://www.cern.ch:8',
            'http://www.cern.ch:80',
            'http://www.cern.ch:800',
            'http://www.cern.ch:8000',
            'http://www.cern.ch:'
        ]
        
        self.urlssec = [
            'https://www.cern.ch/',
            'https://www.cern.ch:8/',
            'https://www.cern.ch:80/',
            'https://www.cern.ch:800/',
            'https://www.cern.ch:8000/',
            'https://www.cern.ch:',
            'https://www.cern.ch',
            'https://www.cern.ch:8',
            'https://www.cern.ch:80',
            'https://www.cern.ch:800',
            'https://www.cern.ch:8000',
            'https://www.cern.ch:/'
        ]
        
        self.srms = [
            'srm:castor.cern.ch:8443/dasdsa//ddsa////dasdsadas',
            'srm:/castor.cern.ch:8443/dasdsa//ddsa////dasdsadas',
            'srm://castor.cern.ch/dsfds//32dsadsa/',
            'srm://castor.cern.ch:1/dsfds//32dsadsa/',
            'srm://castor.cern.ch:12/dsfds//32dsadsa/',
            'srm://castor.cern.ch:123/dsfds//32dsadsa/',            
            'srm://castor.cern.ch:1234/dsfds//32dsadsa/',
            'srm://castor.cern.ch:12345/dsfds//32dsadsa/',
            'srm://///castor.cern.ch:8443//fdsfdsfd/fds//f/dfdsafsa'
        ]


# PUBLIC methods


    def setUp (self):
        """
        @since: 0.2.2
        """
        pass


    def tearDown (self):
        """
        @since: 0.2.2
        """
        pass


    def test_ping (self):
        """
        Tests dq2.common.DQPing.ping method.
        
        @since: 0.2.2
        
        
        # 1. test entering valid IP addresses
        # 1.1 test entering loopback interface
        # 1.2 test entering unknown host
        """
        
        result = dq2.common.DQPing.ping(self.ip_valid)
        expected = 2
        self.assertEqual(result, expected, self._fmt_message('1.1', expected, result))
        
        result = dq2.common.DQPing.ping(self.ip_unknown_host)
        expected = 0
        self.assertEqual(result, expected, self._fmt_message('1.2', expected, result))


    def test_ping_response (self):
        """
        Tests dq2.common.DQPing.ping_response method.
        
        @since: 0.2.2
        
        
        # 1. test entering valid parameters
        # 1.1 test entering empty string
        """
        pass


    def test_pings (self):
        """
        Tests dq2.common.DQPing.pings method.
        
        @since: 0.2.2
        
        
        # 1.1 test entering a loopback interface twice
        # 1.2 test entering the loopback interface and a unknown host
        # 1.3 test entering an unknown host twice
        """
        
        result = dq2.common.DQPing.pings([self.ip_valid, self.ip_valid])
        expected = {self.ip_valid: 2}
        self.assertEqual(result, expected, self._fmt_message('1.1', expected, result))
        
        result = dq2.common.DQPing.pings([self.ip_valid, self.ip_unknown_host])
        expected = {self.ip_valid: 2, self.ip_unknown_host: 0}
        self.assertEqual(result, expected, self._fmt_message('1.2', expected, result))
        
        result = dq2.common.DQPing.pings([self.ip_unknown_host, self.ip_unknown_host])
        expected = {self.ip_unknown_host: 0}
        self.assertEqual(result, expected, self._fmt_message('1.3', expected, result))


    def test_getHostname (self):
        """
        Tests dq2.common.DQPing.getHostname method.
        
        @since: 0.2.2
        
        
        # 1. test entering valid host names
        # 1.1 test with http URLs
        # 1.2 test with https URLs
        # 1.3 test with srm URLs
        """
        
        for eachURL in self.urls:
            result = dq2.common.DQPing.getHostname(eachURL)
            expected = 'www.cern.ch'
            self.assertEqual(result, expected, self._fmt_message('1.1 : '+ eachURL, expected, result))
        
        for eachURL in self.urlssec:
            result = dq2.common.DQPing.getHostname(eachURL)
            expected = 'www.cern.ch'
            self.assertEqual(result, expected, self._fmt_message('1.2 : '+ eachURL, expected, result))
        
        for eachURL in self.srms:
            result = dq2.common.DQPing.getHostname(eachURL)
            expected = 'castor.cern.ch'
            self.assertEqual(result, expected, self._fmt_message('1.3 : '+ eachURL, expected, result))


if __name__ == '__main__':
    """
    Runs all tests in DQPingTestCase.
    
    @since: 0.2.2
    """
import unittest
suite = unittest.makeSuite(DQPingTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)