"""
Testcase for the dq2.common.DQValidator module.

@author: Pedro Salgado
@contact: pedro.salgado@cern.ch
@since: 0.2
@version: $Id: DQValidatorTestCase.py,v 1.3 2010-10-12 08:07:10 vgaronne Exp $
"""

import dq2.common.validator
import dq2.common.validator.testcase.data

from dq2.common.constants import *
from dq2.common.DQException import DQInvalidRequestException, DQNonFatalError, DQUserError
import dq2.common
from dq2.common.testcase.DQTestCase import DQTestCase


class DQValidatorTestCase (DQTestCase):
    """
    Testcase for the dq2.common.DQValidator module.
    
    @author: Pedro Salgado
    @contact: pedro.salgado@cern.ch
    @since: 0.2
    @version: $Revision: 1.3 $
    """


    def __init__ (self, name):
        """
        Constructs an instance of DQValidatorTestCase.
        
        @author: Pedro Salgado
        @contact: pedro.salgado@cern.ch
        @since: 0.2
        
        @param name: testcase name.
        @type name: str
        """
        DQTestCase.__init__(self, name)
        
        self.param_date = dq2.common.validator.testcase.data.dates
        self.param_invalid_date = dq2.common.validator.testcase.data.dates_invalid
        
        self.param_dict_0 = {}
        
        self.param_int__1 = -1
        self.param_int_0 = 0
        self.param_int_1 = 1
        
        self.param_lst_0 = []
        
        self.param_md5_01 = 'md5:9cf3329655f1bbe73340f7a60b0ff76c'
        self.param_md5_02 = 'md5:ac5cf111f8300aa97ddc01842587f46b'
        
        self.param_invalid_md5_36 = 'md5:9cf3329655f1bbe73340f7a60b0ff76g'
        
        self.param_invalid_site_0 = '<invalid_site>'
        
        self.param_str_0 = ''
        self.param_str_1 = '1'
        self.param_str_10 = 'A' * 10
        self.param_str_11 = 'A' * 11
        self.param_str_20 = 'A' * 20
        self.param_str_36 = 'A' * 36
        self.param_str_37 = 'A' * 37
        self.param_str_50 = 'A' * 50
        self.param_str_51 = 'A' * 51
        self.param_str_132 = 'A' * 133
        self.param_str_133 = 'A' * 134
        self.param_str_255 = 'A' * 255
        self.param_str_256 = 'A' * 256
        self.param_str_512 = 'A' * 512
        self.param_str_513 = 'A' * 513
        self.param_str = [
            self.param_str_0,
            self.param_str_1,
            self.param_str_10,
            self.param_str_11,
            self.param_str_20,
            self.param_str_36,
            self.param_str_37,
            self.param_str_50,
            self.param_str_51,
            self.param_str_132,
            self.param_str_133,
            self.param_str_255,
            self.param_str_256,
            self.param_str_512,
            self.param_str_513
        ]
        
        self.param_invalid_dsn_0 = 'dqtest/invalid/name'
        
        self.param_invalid_lfn_0 = 'dqtest/invalid/name'
        
        self.param_owner = dq2.common.validator.testcase.data.owners
        
        self.param_tpl_0 = ()
        
        self.param_uuid_01 = dq2.common.generate_uuid()
        self.param_uuid_02 = '90c2a03b-5526-4616-8283-7d9d20c0214b'
        
        self.param_url_00 = 'http://www.cern.ch/'
        self.param_url_01 = 'http://www.cern.ch:8/'
        self.param_url_02 = 'http://www.cern.ch:80/'
        self.param_url_03 = 'http://www.cern.ch:800/'
        self.param_url_04 = 'http://www.cern.ch:8000/'
        self.param_url_05 = 'http://www.cern.ch:/'
        self.param_url_10 = 'http://www.cern.ch'
        self.param_url_11 = 'http://www.cern.ch:8'
        self.param_url_12 = 'http://www.cern.ch:80'
        self.param_url_13 = 'http://www.cern.ch:800'
        self.param_url_14 = 'http://www.cern.ch:8000'
        self.param_url_15 = 'http://www.cern.ch:'
        self.param_url = [
            self.param_url_00,
            self.param_url_01,
            self.param_url_02,
            self.param_url_03,
            self.param_url_04,
            self.param_url_05,
            self.param_url_10,
            self.param_url_11,
            self.param_url_12,
            self.param_url_13,
            self.param_url_14,
            self.param_url_15
        ]
        
        
        self.param_urlsec_00 = 'https://www.cern.ch/'
        self.param_urlsec_01 = 'https://www.cern.ch:8/'
        self.param_urlsec_02 = 'https://www.cern.ch:80/'
        self.param_urlsec_03 = 'https://www.cern.ch:800/'
        self.param_urlsec_04 = 'https://www.cern.ch:8000/'
        self.param_urlsec_05 = 'https://www.cern.ch:'
        self.param_urlsec_10 = 'https://www.cern.ch'
        self.param_urlsec_11 = 'https://www.cern.ch:8'
        self.param_urlsec_12 = 'https://www.cern.ch:80'
        self.param_urlsec_13 = 'https://www.cern.ch:800'
        self.param_urlsec_14 = 'https://www.cern.ch:8000'
        self.param_urlsec_15 = 'https://www.cern.ch:/'
        self.param_urlsec = [
            self.param_urlsec_00,
            self.param_urlsec_01,
            self.param_urlsec_02,
            self.param_urlsec_03,
            self.param_urlsec_04,
            self.param_urlsec_05,
            self.param_urlsec_10,
            self.param_urlsec_11,
            self.param_urlsec_12,
            self.param_urlsec_13,
            self.param_urlsec_14,
            self.param_urlsec_15
        ]
        
        self.param_invalid_url_0 = 'htp://www.cern.ch:/'
        self.param_invalid_url_1 = 'htps://www.cern.ch:/'
        
        self.param_with_blanks_0 = ' A'
        self.param_with_blanks_1 = 'A A'
        self.param_with_blanks_2 = 'AA '
        self.param_with_blanks = [
            self.param_with_blanks_0,
            self.param_with_blanks_1,
            self.param_with_blanks_2
        ]
        
        self.param_with_slash_0 = '/'
        self.param_with_slash_1 = 'AA/'
        self.param_with_slash_2 = '/AA'
        self.param_with_slash_3 = 'A/A'
        self.param_with_slash = [
            self.param_with_slash_0,
            self.param_with_slash_1,
            self.param_with_slash_2,
            self.param_with_slash_3
        ]
        
        self.param_with_backslash_0 = '\\'
        self.param_with_backslash_1 = '\\AA'
        self.param_with_backslash_2 = 'AA\\'
        self.param_with_backslash_3 = 'A\\A'
        self.param_with_backslash = [
            self.param_with_backslash_0,
            self.param_with_backslash_1,
            self.param_with_backslash_2,
            self.param_with_backslash_3
        ]

        self.param_with_at_0 = "@"
        self.param_with_at_1 = "@A"
        self.param_with_at_2 = "A@"
        self.param_with_at_3 = "A@A"
        self.param_with_at = [
            self.param_with_at_0,
            self.param_with_at_1,
            self.param_with_at_2,
            self.param_with_at_3
        ]     
        
        self.param_date_criteria_0 = '<>'


# PUBLIC methods


    def setUp (self):
        """
        @since: 0.2.1
        """
        pass


    def tearDown (self):
        """
        @since: 0.2.1
        """
        pass


    def test_is_dataset_name (self):
        """
        Tests dq2.common.DQValidator.is_dataset_name method.
        
        @since: 0.2.1
        
        # 1. test entering valid parameters
        # 1.1 test entering a 255-character string
        # 2. test entering invalid parameters
        # 2.1 test entering a 256-character string
        # 2.2 test entering an integer
        # 2.3 test entering a list
        # 2.4 test entering a dictionary
        # 2.5 test entering a tuple
        # 2.6 test entering a string with blank spaces
        # 2.7 test entering empty string
        # 2.8 test entering an invalid dataset name
        """
        
        # 1. test entering valid parameters
        expected = None
        
        # 1.1 test entering a 255-character string
        result = dq2.common.validator.is_dataset_name([self.param_str_255])
        self.assertEqual(result, expected, self._fmt_message('1.1', expected, result))
        
        
        # 2. test entering invalid parameters
        expected = 'DQInvalidRequestException'
        
        # 2.1 test entering a 256-character string
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_dataset_name,
            [self.param_str_256]
        )
        
        # 2.2 test entering an integer
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_dataset_name,
            [self.param_int_0]
        )
        
        # 2.3 test entering a list
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_dataset_name,
            [self.param_lst_0]
        )
        
        # 2.4 test entering a dictionary
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_dataset_name,
            [self.param_dict_0]
        )
        
        # 2.5 test entering a tuple
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_dataset_name,
            [self.param_tpl_0]
        )
        
        # 2.6 test entering a string with blank spaces
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_dataset_name,
            [self.param_with_blanks_0]
        )
        
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_dataset_name,
            [self.param_with_blanks_1]
        )
        
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_dataset_name,
            [self.param_with_blanks_2]
        )
        
        # 2.7 test entering empty string
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_dataset_name,
            [self.param_str_0]
        )
        
        # 2.8 test entering an invalid dataset name
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_dataset_name,
            [self.param_invalid_dsn_0]
        )


    def test_is_dataset_name_strict (self):
        """
        Tests dq2.common.DQValidator.is_dataset_name_strict method.
        
        @since: 1.0.0
        
        # 1. test entering valid parameters
        # 1.1 test entering a 255-character string
        # 2. test entering invalid parameters
        # 2.1 test entering a 256-character string
        # 2.2 test entering an integer
        # 2.3 test entering a list
        # 2.4 test entering a dictionary
        # 2.5 test entering a tuple
        # 2.6 test entering a string with blank spaces
        # 2.7 test entering empty string
        # 2.8 test entering an invalid dataset name
        """
        
        # 1. test entering valid parameters
        expected = None
        
        # 1.1 test entering a 255-character string
        result = dq2.common.validator.is_dataset_name_strict([self.param_str_255])
        self.assertEqual(result, expected, self._fmt_message('1.1', expected, result))
        
        
        # 2. test entering invalid parameters
        expected = 'DQInvalidRequestException'
        
        # 2.1 test entering a 256-character string
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_dataset_name_strict,
            [self.param_str_256]
        )
        
        # 2.2 test entering an integer
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_dataset_name_strict,
            [self.param_int_0]
        )
        
        # 2.3 test entering a list
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_dataset_name_strict,
            [self.param_lst_0]
        )
        
        # 2.4 test entering a dictionary
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_dataset_name_strict,
            [self.param_dict_0]
        )
        
        # 2.5 test entering a tuple
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_dataset_name_strict,
            [self.param_tpl_0]
        )
        
        # 2.6 test entering a string with blank spaces
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_dataset_name_strict,
            [self.param_with_blanks_0]
        )
        
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_dataset_name_strict,
            [self.param_with_blanks_1]
        )
        
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_dataset_name_strict,
            [self.param_with_blanks_2]
        )
        
        # 2.7 test entering empty string
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_dataset_name_strict,
            [self.param_str_0]
        )
        
        # 2.8 test entering an invalid dataset name
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_dataset_name_strict,
            [self.param_invalid_dsn_0]
        )


    def test_is_dataset_state (self):
        """
        Tests dq2.common.validator.is_dataset_state method.
        
        @since: 0.2.1
        
        # 1. test entering valid parameters
        # 1.1 test all valid dq2.common.constants.DatasetState.STATES
        # 2. test entering invalid parameters
        # 2.1 test entering an invalid state
        # 2.2 test entering a string
        # 2.3 test entering a list
        # 2.4 test entering a dictionary
        # 2.5 test entering a tuple
        """
        
        # 1. test entering valid parameters
        
        # 1.1 test all valid dq2.common.constants.DatasetState.STATES
        expected = None
        
        for eachState in DatasetState.STATES:
            result = dq2.common.validator.is_dataset_state([eachState])
            self.assertEqual(result, expected, self._fmt_message('1.1', expected, result))
        
        
        # 2. test entering invalid parameters
        
        # 2.1 test entering an invalid state
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_dataset_state,
            [self.param_int__1]
        )
        
        # 2.2 test entering a string
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_dataset_state,
            [self.param_str_0]
        )
        
        # 2.3 test entering a list
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_dataset_state,
            [self.param_lst_0]
        )
        
        # 2.4 test entering a dictionary
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_dataset_state,
            [self.param_dict_0]
        )
        
        # 2.5 test entering a tuple
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_dataset_state,
            [self.param_tpl_0]
        )


    def test_is_date (self):
        """
        Tests dq2.common.validator.is_date method.
        
        @since: 0.2.1
        
        # 1. test entering valid parameters
        # 2. test entering invalid parameters
        # 2.1 test entering a 20-character string
        # 2.2 test entering an integer
        # 2.3 test entering a list
        # 2.4 test entering a dictionary
        # 2.5 test entering a tuple
        # 2.6 test entering a string with blank spaces
        # 2.7 test entering an invalid MD5 32-character string
        # 2.8 test entering empty string
        """
        
        # 1. test entering valid parameters
        
        # 1.1 test entering a real date
        expected = None
        
        for eachDate in self.param_date:
            result = dq2.common.validator.is_date([eachDate])
            self.assertEqual(result, expected, self._fmt_message('1.1', expected, result))
        
        for eachDate in self.param_invalid_date:
            self.assertRaises(
                DQInvalidRequestException,
                dq2.common.validator.is_date,
                [eachDate]
            )
        
        
        # 2. test entering invalid parameters
        expected = 'DQInvalidRequestException'
        
        # 2.1 test entering a 20-character string
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_date,
            [self.param_str_20]
        )
        
        # 2.2 test entering an integer
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_date,
            [self.param_int_0]
        )
        
        # 2.3 test entering a list
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_date,
            [self.param_lst_0]
        )
        
        # 2.4 test entering a dictionary
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_date,
            [self.param_dict_0]
        )
        
        # 2.5 test entering a tuple
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_date,
            [self.param_tpl_0]
        )
        
        # 2.6 test entering a string with blank spaces
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_date,
            [self.param_with_blanks_0]
        )
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_date,
            [self.param_with_blanks_1]
        )
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_date,
            [self.param_with_blanks_2]
        )
        
        # 2.7 test entering an invalid MD5 36-character string
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_date,
            [self.param_invalid_md5_36]
        )
        
        # 2.8 test entering empty string
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_date,
            [self.param_str_0]
        )


    def test_is_date_criteria (self):
        """
        Tests dq2.common.validator.is_date_criteria  method.
        
        @since: 0.3.0
        
        # 1. test entering valid parameters
        # 1.1 test all valid dq2.common.constants.DateCriteria.__ALL__
        # 2. test entering invalid parameters
        # 2.1 test entering an invalid criteria
        """
        
        # 1. test entering valid parameters
        
        # 1.1 test all valid dq2.common.constants.DateCriteria.__ALL__
        expected = None
        
        for eachCriteria in DateCriteria.__ALL__:
            result = dq2.common.validator.is_date_criteria([eachCriteria])
            self.assertEqual(result, expected, self._fmt_message('1.1', expected, result))
        
        
        # 2. test entering invalid parameters
        
        # 2.1 test entering an invalid criteria
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_date_criteria,
            [self.param_date_criteria_0]
        )


    def test_is_lfn (self):
        """
        Tests dq2.common.validator.is_lfn
        
        @since: 0.3.0
        
        # 1. test entering valid parameters
        # 1.1 test entering a 255-character string
        # 2. test entering invalid parameters
        # 2.1 test entering a 256-character string
        # 2.2 test entering an integer
        # 2.3 test entering a list
        # 2.4 test entering a dictionary
        # 2.5 test entering a tuple
        # 2.6 test entering a string with blank spaces
        # 2.7 test entering empty string
        # 2.8 test entering an invalid dataset name
        # 2.9 test entering a string with a slash
        # 2.10 test entering a string with backslash
        # 2.11 test entering a string with @
        """
        
        # 1. test entering valid parameters
        expected = None
        
        # 1.1 test entering a 255-character string
        message = '1.1 test entering a 255-character string'
        result = dq2.common.validator.is_lfn([self.param_str_255])
        self.assertEqual(result, expected, self._fmt_message(message, expected, result))
        
        
        # 2. test entering invalid parameters
        expected = 'DQInvalidRequestException'
        
        # 2.1 test entering a 256-character string
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_lfn,
            [self.param_str_256]
        )
        
        # 2.2 test entering an integer
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_lfn,
            [self.param_int_0]
        )
        
        # 2.3 test entering a list
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_lfn,
            [self.param_lst_0]
        )
        
        # 2.4 test entering a dictionary
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_lfn,
            [self.param_dict_0]
        )
        
        # 2.5 test entering a tuple
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_lfn,
            [self.param_tpl_0]
        )
        
        # 2.6 test entering a string with blank spaces
        for param in self.param_with_blanks:
            self.assertRaises(
                DQInvalidRequestException,
                dq2.common.validator.is_lfn,
                [param]
            )
        
        # 2.7 test entering empty string
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_lfn,
            [self.param_str_0]
        )
        
        # 2.8 test entering an invalid dataset name
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_lfn,
            [self.param_invalid_dsn_0]
        )
        
        # 2.9 test entering a string with a slash
        for param in self.param_with_slash:
            self.assertRaises(
                DQInvalidRequestException,
                dq2.common.validator.is_lfn,
                [param]
            )
        
        # 2.10 test entering a string with backslash
        for param in self.param_with_backslash:
            self.assertRaises(
                DQInvalidRequestException,
                dq2.common.validator.is_lfn,
                [param]
            )
        
        # 2.11 test entering a string with @
        for param in self.param_with_at:
            self.assertRaises(
                DQInvalidRequestException,
                dq2.common.validator.is_lfn,
                [param]
            )


    def test_is_http_url (self):
        """
        Tests dq2.common.validator.is_http_url method.
        @since: 0.2.1
        
        # 1. test entering valid parameters
        # 1.1 test entering a real URLs
        # 2. test entering invalid parameters
        # 2.1 test entering an integer
        # 2.2 test entering a list
        # 2.3 test entering a dictionary
        # 2.4 test entering a tuple
        # 2.5 test entering empty string
        # 2.6 test entering invalid URLs
        """
        
        # 1. test entering valid parameters
        
        # 1.1 test entering a real UID
        for eachURL in [
            self.param_url_00,
            self.param_url_01,
            self.param_url_02,
            self.param_url_03,
            self.param_url_04,
            self.param_url_05,
            self.param_url_10,
            self.param_url_11,
            self.param_url_12,
            self.param_url_13,
            self.param_url_14,
            self.param_url_15,
            
            self.param_urlsec_00,
            self.param_urlsec_01,
            self.param_urlsec_02,
            self.param_urlsec_03,
            self.param_urlsec_04,
            self.param_urlsec_05,
            self.param_urlsec_10,
            self.param_urlsec_11,
            self.param_urlsec_12,
            self.param_urlsec_13,
            self.param_urlsec_14,
            self.param_urlsec_15
        ]:
            expected = None
            result = dq2.common.validator.is_http_url([eachURL])
            self.assertEqual(result, expected, self._fmt_message('1.1', expected, result))
        
        
        # 2. test entering invalid parameters
        expected = 'DQInvalidRequestException'
        
        # 2.1 test entering an integer
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_http_url,
            [self.param_int_0]
        )
        
        # 2.2 test entering a list
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_http_url,
            [self.param_lst_0]
        )
        
        # 2.3 test entering a dictionary
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_http_url,
            [self.param_dict_0]
        )
        
        # 2.4 test entering a tuple
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_http_url,
            [self.param_tpl_0]
        )
        
        # 2.5 test entering empty string
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_http_url,
            [self.param_str_0]
        )
        
        # 2.6 test entering invalid URLs
        for eachURL in [
            self.param_invalid_url_0,
            self.param_invalid_url_1
        ]:
            self.assertRaises(
                DQInvalidRequestException,
                dq2.common.validator.is_http_url,
                [eachURL]
            )


    def test_is_md5 (self):
        """
        Tests dq2.common.validator.is_md5 method.
        
        @since: 0.2.1
        
        # 1. test entering valid parameters
        # 2. test entering invalid parameters
        # 2.1 test entering a 36-character string
        # 2.2 test entering an integer
        # 2.3 test entering a list
        # 2.4 test entering a dictionary
        # 2.5 test entering a tuple
        # 2.6 test entering a string with blank spaces
        # 2.7 test entering an invalid MD5 36-character string
        # 2.8 test entering empty string
        # 2.9 test entering a 37-character string
        """
        
        # 1. test entering valid parameters
        
        # 1.1 test entering a real UID
        expected = None
        result = dq2.common.validator.is_md5([self.param_md5_01])
        self.assertEqual(result, expected, self._fmt_message('1.1', expected, result))
        
        result = dq2.common.validator.is_md5([self.param_md5_02])
        self.assertEqual(result, expected, self._fmt_message('1.1', expected, result))
        
        
        # 2. test entering invalid parameters
        expected = 'DQInvalidRequestException'
        
        # 2.1 test entering a 36-character string
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_md5,
            [self.param_str_36]
        )
        
        # 2.2 test entering an integer
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_md5,
            [self.param_int_0]
        )
        
        # 2.3 test entering a list
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_md5,
            [self.param_lst_0]
        )
        
        # 2.4 test entering a dictionary
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_md5,
            [self.param_dict_0]
        )
        
        # 2.5 test entering a tuple
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_md5,
            [self.param_tpl_0]
        )
        
        # 2.6 test entering a string with blank spaces
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_md5,
            [self.param_with_blanks_0]
        )
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_md5,
            [self.param_with_blanks_1]
        )
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_md5,
            [self.param_with_blanks_2]
        )
        
        # 2.7 test entering an invalid MD5 36-character string
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_md5,
            [self.param_invalid_md5_36]
        )
        
        # 2.8 test entering empty string
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_md5,
            [self.param_str_0]
        )
        
        # 2.9 test entering a 37-character string
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_md5,
            [self.param_str_37]
        )


    def test_is_metadata_attribute (self):
        """
        Tests dq2.common.validator.is_metadata_attribute method.
        @since: 0.2.1

        # 1. test entering valid parameters
        # 1.1 test entering dq2.common.constants.Metadata.ATTRIBUTES
        # 2. test entering invalid parameters
        # 2.1 test entering a None value
        # 2.2 test entering an empty string
        # 2.3 test entering an non-metadata attribute string
        # 2.4 test entering an integer
        # 2.5 test entering a list
        # 2.6 test entering a dictionary
        # 2.7 test entering a tuple
        """
        
        # 1. test entering valid parameters
        
        # 1.1 test entering dq2.common.constants.Metadata.ATTRIBUTES
        expected = None
        for eachAttribute in dq2.common.constants.Metadata.DATASET + dq2.common.constants.Metadata.DATASET_VERSION + dq2.common.constants.Metadata.USER_VERSION:
            result = dq2.common.validator.is_metadata_attribute([eachAttribute])
            self.assertEqual(result, expected, self._fmt_message('1.1 test entering dq2.common.constants.Metadata.ATTRIBUTES', expected, result))
        
        
        # 2. test entering invalid parameters
        
        # 2.1 test entering a None value
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_metadata_attribute,
            [None]
        )
        
        # 2.2 test entering an empty string
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_metadata_attribute,
            [self.param_str_0]
        )
        
        # 2.3 test entering an non-metadata attribute string
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_metadata_attribute,
            [self.param_str_10]
        )
        
        # 2.4 test entering an integer
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_metadata_attribute,
            [self.param_int_0]
        )
        
        # 2.5 test entering a list
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_metadata_attribute,
            [self.param_lst_0]
        )
        
        # 2.6 test entering a dictionary
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_metadata_attribute,
            [self.param_dict_0]
        )
        
        # 2.7 test entering a tuple
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_metadata_attribute,
            [self.param_tpl_0]
        )


    def test_is_owner (self):
        """
        Tests dq2.common.DQValidator.is_owner method.
        @since: 0.2.1

        # 1. test entering valid parameters
        # 1.1 test entering valid owner
        # 2. test entering invalid parameters
        # 2.1 test entering an invalid owner
        # 2.2 test entering an integer
        # 2.3 test entering a list
        # 2.4 test entering a dictionary
        # 2.5 test entering a tuple
        # 2.6 test entering a string with blank spaces
        # 2.7 test entering empty string
        """
        
        # 1. test entering valid parameters
        expected = None
        
        # 1.1 test entering a valid owner
        for owner in self.param_owner:
            result = dq2.common.validator.is_owner([owner])
            self.assertEqual(result, expected, self._fmt_message('1.1', expected, result))
        
        
        # 2. test entering invalid parameters
        expected = 'DQInvalidRequestException'
        
        # 2.1 test entering an invalid owner
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_owner,
            [self.param_str_256]
        )
        
        # 2.2 test entering an integer
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_owner,
            [self.param_int_0]
        )

        # 2.3 test entering a list
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_owner,
            [self.param_lst_0]
        )

        # 2.4 test entering a dictionary
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_owner,
            [self.param_dict_0]
        )

        # 2.5 test entering a tuple
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_owner,
            [self.param_tpl_0]
        )

        # 2.6 test entering a string with blank spaces
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_owner,
            [self.param_with_blanks_0]
        )
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_owner,
            [self.param_with_blanks_1]
        )
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_owner,
            [self.param_with_blanks_2]
        )

        # 2.7 test entering empty string
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_owner,
            [self.param_str_0]
        )


    def test_is_pfn (self):
        """
        Tests dq2.common.validator.is_pfn
        @since: 0.3.0
        
        # 1. test entering valid parameters
        # 1.1 test entering a 512-character string
        # 2. test entering invalid parameters
        # 2.1 test entering a 513-character string
        # 2.2 test entering an integer
        # 2.3 test entering a list
        # 2.4 test entering a dictionary
        # 2.5 test entering a tuple
        # 2.6 test entering a string with blank spaces
        # 2.7 test entering empty string
        # 2.9 test entering a string with backslash
        # 2.10 test entering a string with @
        """

        # 1. test entering valid parameters
        expected = None

        # 1.1 test entering a 512-character string
        message = '1.1 test entering a 512-character string'
        result = dq2.common.validator.is_pfn([self.param_str_512])
        self.assertEqual(result, expected, self._fmt_message(message, expected, result))


        # 2. test entering invalid parameters
        expected = 'DQInvalidRequestException'

        # 2.1 test entering a 513-character string
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_pfn,
            [self.param_str_513]
        )

        # 2.2 test entering an integer
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_pfn,
            [self.param_int_0]
        )

        # 2.3 test entering a list
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_pfn,
            [self.param_lst_0]
        )

        # 2.4 test entering a dictionary
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_pfn,
            [self.param_dict_0]
        )

        # 2.5 test entering a tuple
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_lfn,
            [self.param_tpl_0]
        )

        # 2.6 test entering a string with blank spaces
        for param in self.param_with_blanks:
            self.assertRaises(
                DQInvalidRequestException,
                dq2.common.validator.is_pfn,
                [param]
            )

        # 2.7 test entering empty string
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_pfn,
            [self.param_str_0]
        )

        # 2.8 test entering a string with backslash
        for param in self.param_with_backslash:
            self.assertRaises(
                DQInvalidRequestException,
                dq2.common.validator.is_pfn,
                [param]
            )

        # 2.9 test entering a string with @
        for param in self.param_with_at:
            self.assertRaises(
                DQInvalidRequestException,
                dq2.common.validator.is_pfn,
                [param]
            )


    def test_is_uid (self):
        """
        Tests dq2.common.validator.is_uid method.
        @since: 0.2.1
        
        # 1. test entering valid parameters
        # 1.1 test entering a real UID
        # 2. test entering invalid parameters
        # 2.1 test entering a 37-character string
        # 2.2 test entering an integer
        # 2.3 test entering a list
        # 2.4 test entering a dictionary
        # 2.5 test entering a tuple
        # 2.6 test entering a string with blank spaces
        # 2.7 test entering an invalid UID 36-character string
        # 2.8 test entering empty string
        """
        
        # 1. test entering valid parameters
        
        # 1.1 test entering a real UID
        expected = None
        result = dq2.common.validator.is_uid([self.param_uuid_01])
        self.assertEqual(result, expected, self._fmt_message('1.1', expected, result))
        
        result = dq2.common.validator.is_uid([self.param_uuid_02])
        self.assertEqual(result, expected, self._fmt_message('1.1', expected, result))
        
        
        # 2. test entering invalid parameters
        expected = 'DQInvalidRequestException'
        
        # 2.1 test entering a 256-character string
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_uid,
            [self.param_str_37]
        )
        
        # 2.2 test entering an integer
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_uid,
            [self.param_int_0]
        )
        
        # 2.3 test entering a list
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_uid,
            [self.param_lst_0]
        )
        
        # 2.4 test entering a dictionary
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_uid,
            [self.param_dict_0]
        )
        
        # 2.5 test entering a tuple
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_uid,
            [self.param_tpl_0]
        )
        
        # 2.6 test entering a string with blank spaces
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_uid,
            [self.param_with_blanks_0]
        )
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_uid,
            [self.param_with_blanks_1]
        )
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_uid,
            [self.param_with_blanks_2]
        )
        
        # 2.7 test entering an invalid UID 36-character string
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_uid,
            [self.param_str_36]
        )
        
        # 2.8 test entering empty string
        self.assertRaises(
            DQInvalidRequestException,
            dq2.common.validator.is_uid,
            [self.param_str_0]
        )


    def test_except_statements (self):
        """
        @since: 0.3.0
        """
        
        err_msg = 'DQInvalidRequestException should be a kind of DQNonFatalError!'
        
        try:
            dq2.common.validator.is_uid([self.param_str_36])
        except DQNonFatalError as e:
            pass
        except:
            self.fail(err_msg)
        
        try:
            dq2.common.validator.is_uid([self.param_str_36])
        except DQNonFatalError as e:
            pass
        except:
            self.fail(err_msg)
            
        err_msg = 'DQInvalidRequestException should be a kind of DQUserError!'
        
        try:
            dq2.common.validator.is_uid([self.param_str_36])
        except DQUserError as e:
            pass
        except:
            self.fail(err_msg)
            
        try:
            dq2.common.validator.is_uid([self.param_str_36])
        except DQUserError as e:
            pass
        except:
            self.fail(err_msg)


    def test_not_all_none (self):
        """
        @since: 0.3.0
        """
        
        self.assertEqual(dq2.common.validator.not_all_none(['abc', None]), None)
        self.assertEqual(dq2.common.validator.not_all_none([None, 'abc']), None)
        self.assertEqual(dq2.common.validator.not_all_none(['abc']), None)
        self.assertRaises(DQInvalidRequestException,
                          dq2.common.validator.not_all_none,
                          'abc')
        self.assertRaises(DQInvalidRequestException,
                          dq2.common.validator.not_all_none,
                          [None])
        self.assertRaises(DQInvalidRequestException,
                          dq2.common.validator.not_all_none,
                          [None, None])


if __name__ == '__main__':
    """
    Runs all tests in DQValidatorTestCase.
    
    @since: 0.2.1
    """
    import sys
    
    test = DQValidatorTestCase.main(
        'dq2.common.validator.testcase', 'DQValidatorTestCase',
        sys.argv[1:]
    )
