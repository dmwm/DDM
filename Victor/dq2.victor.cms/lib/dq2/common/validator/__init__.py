"""
DQ2 common validation methods.

@author: Pedro Salgado
@contact: pedro.salgado@cern.ch
@since: 0.2.2
@version: $Id: __init__.py,v 1.17 2010-10-04 13:24:11 vgaronne Exp $

@warning: since these methods should be able to validate a list of parameters the types should *also* be checked
on the validation aspect itself not only in this module.
"""


__version__ = '$Name: not supported by cvs2svn $'


import datetime
import re
import string


from dq2.common.constants import DatasetState, DateCriteria, Metadata
from dq2.common.DQException import DQInvalidRequestException


ADLER32_REGEXP                = '^ad:[a-fA-F0-9]{8}$'
ADLER32_COMPILED_REGEXP       = re.compile(ADLER32_REGEXP)
DATASET_LOCATION_MAXLENGTH    = 50
DATASET_NAME_MAXLENGTH        = 255
DATASET_NAME_STRICT_MAXLENGTH = 132
DATE_REGEXP                   = '^[1-9]{1}[0-9]{3}-[0-9]{1,2}-[0-9]{1,2}( [0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2})?$'
DATE_COMPILED_REGEXP          = re.compile(DATE_REGEXP)
LFN_MAXLENGTH                 = 255
MD5_MAXLENGTH                 = 36
MD5_REGEXP                    = '^md5:[a-fA-F0-9]{32}$'
MD5_COMPILED_REGEXP           = re.compile(MD5_REGEXP)
METADATA_VALUE_MAXLENGTH      = 10
PFN_MAXLENGTH                 = 512
UID_MAXLENGTH                 = 36
UID_REGEXP                    = '^\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$'
UID_COMPILED_REGEXP           = re.compile(UID_REGEXP)
URL_REGEXP                    = '^http(s)?://[^ ]+(:\d{1,4})?(/)?$'
URL_COMPILED_REGEXP           = re.compile(URL_REGEXP)


def dict_has_keys (dictionary, keys):
    """
    Tests if the given dictionary has all of the given keys.
    
    @since: 0.3.0
    
    dictionary is the dictionary to be tested.
    keys are the dictionary keys to be tested.
    
    DQInvalidRequestException is raised,
    in case the given dictionary doesn't have at least one of the given keys.
    """
    is_dictionary([dictionary])
    
    for eachKey in keys:
        if not dictionary.has_key(eachKey):
            err_msg = 'Dictionary is missing key %s!' % (eachKey)
            raise DQInvalidRequestException(err_msg)


def has_no_blank_spaces (args):
    """
    Make sure all arguments don't have any blank spaces.
    
    @since: 0.2.0
    
    @param args: is the list of arguments to be tested.
    
    B{Exceptions}
        - DQInvalidRequestException is raised,
            in case, at least, one of the arguments has a blank space.
    """
    
    for arg in args:
        if string.find(arg, ' ') >= 0:
            err_msg = "Blank spaces are not allowed in this parameter [%s]!" % (str(arg))
            raise DQInvalidRequestException(err_msg)


def has_characters (args, characters):
    """
    @since: 0.3.0
    
    @param args: is the list of arguments to be tested.
    
    B{Exceptions}
        - DQInvalidRequestException is raised,
            in case, at least, one of the arguments has a blank space.
    """
    
    for arg in args:
        for character in characters:
            if string.find(arg, character) >= 0:
                err_msg = "%s character isn't allowed in this parameter [%s]!" % (character, str(arg))
                raise DQInvalidRequestException(err_msg)


def has_slashes (args):
    """
    Make sure all arguments don't have any slash or backslash.
    
    @since: 0.2.0
    
    @param args: is the list of arguments to be tested.
    
    B{Exceptions}
        - DQInvalidRequestException is raised,
            in case, at least, one of the arguments has a slash or backslash.
    """
    return has_characters(args, ['\\', '/'])


def has_wildcard (args):
    """
    Tests if the given arguments have wildcards.
    
    @since: 0.2.11
    
    @param args: is the list of arguments to be tested.
    
    B{Exceptions}
        - DQInvalidRequestException is raised,
            in case, at least, one of the arguments has a wildcard.
    """
    return has_characters(args, ['*'])


def is_boolean (args):
    """
    Make sure all args are bools, if not throw an exception.
    
    @since: 0.2.0
    
    @param args: is the list of arguments to be tested.
    
    B{Exceptions}
        - DQInvalidRequestException is raised,
            in case, at least, one of the arguments is not an bool.
    """
    
    for arg in args:
        if isinstance(arg, int) and (arg >= 0 and arg <= 1):
            continue
        if not isinstance(arg, bool):
            err_msg = '%s is not an bool!' % (str(arg))
            raise DQInvalidRequestException(err_msg)


def is_container_name (args):
    """
    Tests if the given name(s) is a valid dataset name.
    
    @since: 0.2.1
    
    @param args: is the list of arguments to be tested.
    
    B{Exceptions}:
        - DQInvalidRequestException is raised,
            in case the name is not a string or
            if it exceeds the maximum length (dq2.common.DQContants.DATASET_NAME_MAXLENGTH).
    """
    
    for arg in args:
        is_string([arg])
        
        if not arg[-1] == '/':
            """need to add a slash in the end if it's missing"""
            err_msg = "Container name must end with a '/'."
            raise DQInvalidRequestException(err_msg)
        
        if len(arg) == 0:
            err_msg = 'Container name [%s] cannot be an empty string!' % (arg)
            raise DQInvalidRequestException(err_msg)
        
        if len(arg) > DATASET_NAME_STRICT_MAXLENGTH:
            err_msg = 'Container name [%s] exceeds the maximum length (%u)!' % (arg, DATASET_NAME_STRICT_MAXLENGTH)
            raise DQInvalidRequestException(err_msg)
        
        has_characters([arg], ['\\', '@'])
        
        has_no_blank_spaces([arg])


def is_dataset_name (args):
    """
    Tests if the given name(s) is a valid dataset name.
    
    @since: 0.2.1
    
    @param args: is the list of arguments to be tested.
    
    B{Exceptions}:
        - DQInvalidRequestException is raised,
            in case the name is not a string or
            if it exceeds the maximum length (dq2.common.DQContants.DATASET_NAME_MAXLENGTH).
    """
    
    for arg in args:
        is_string([arg])
        
        if len(arg) == 0:
            err_msg = 'Dataset name [%s] cannot be an empty string!' % (arg)
            raise DQInvalidRequestException(err_msg)
        
        if len(arg) > DATASET_NAME_MAXLENGTH:
            err_msg = 'Dataset name [%s] exceeds the maximum length (%u)!' % (arg, DATASET_NAME_MAXLENGTH)
            raise DQInvalidRequestException(err_msg)
        
        has_characters([arg], ['\\', '/', '@'])
        has_no_blank_spaces([arg])


def is_dataset_name_strict (args):
    """
    Tests if the given name(s) is a valid dataset name and if it defines a namespace correctly.
    
    @since: 1.0.0
    
    @param args: is the list of arguments to be tested.
    
    B{Exceptions}:
        - DQInvalidRequestException is raised,
            in case the name is not a string or
            if it exceeds the maximum length (dq2.common.DQContants.DATASET_NAME_STRICT_MAXLENGTH).
    
    @see: http://doc.cern.ch//archive/electronic/cern/others/atlnot/INT/gen/gen-int-2007-001.pdf
    """
    
    for arg in args:
        is_string([arg])
        
        if len(arg) == 0:
            err_msg = 'Dataset name [%s] cannot be an empty string!' % (arg)
            raise DQInvalidRequestException(err_msg)
        
        if len(arg) > DATASET_NAME_STRICT_MAXLENGTH:
            err_msg = 'Dataset name [%s] exceeds the maximum length (%u)!' % (arg, DATASET_NAME_STRICT_MAXLENGTH)
            raise DQInvalidRequestException(err_msg)
        
        pos = arg.find('.')
        
        if pos < 0:
            """dataset name has no dots -> cannot resolve namespace"""
            err_msg = 'Dataset name has to have, at least, one dot! (example: user.<myname>.<name>)!'
            raise DQInvalidRequestException(err_msg)
        
        elif pos == 0:
            """dataset name begins with a dot -> cannot resolve namespace"""
            err_msg = 'Dataset name cannot start with a dot! (example: user.<myname>.<name>)!'
            raise DQInvalidRequestException(err_msg)
        
        elif pos > 15:
            """namespace of a dataset must be <= 15 characters as defined in the ATLAS Dataset Nomenclature document"""
            err_msg = 'First part of a dataset name cannot be more than 15 characters! (example: user.<myname>.<name>)!'
            raise DQInvalidRequestException(err_msg)
        
        has_characters([arg], ['\\', '/', '@'])
        has_no_blank_spaces([arg])


def is_dataset_or_container_name (args):
    """
    Tests if the given name(s) is a valid dataset name.
    
    @since: 0.2.1
    
    @param args: is the list of arguments to be tested.
    
    B{Exceptions}:
        - DQInvalidRequestException is raised,
            in case the name is not a string or
            if it exceeds the maximum length (dq2.common.DQContants.DATASET_NAME_MAXLENGTH).
    """
    
    for arg in args:
        is_string([arg])
        
        if len(arg) == 0:
            err_msg = 'Dataset name [%s] cannot be an empty string!' % (arg)
            raise DQInvalidRequestException(err_msg)
        
        if len(arg) > DATASET_NAME_MAXLENGTH:
            err_msg = 'Dataset name [%s] exceeds the maximum length (%u)!' % (arg, DATASET_NAME_MAXLENGTH)
            raise DQInvalidRequestException(err_msg)
        
        has_characters([arg], ['\\', '@'])
        has_no_blank_spaces([arg])


def is_dataset_state (args):
    """
    Tests if the given state is a valid dataset state (dq2.common.constants.DatasetState).
    
    @since: 0.2.1
    
    @param args: is the list of arguments to be tested.
    
    B{Exceptions}:
        - DQInvalidRequestException is raised,
            in case the state is not an integer or
            if it is an invalid state.  
    """
    
    for arg in args:
        is_integer([arg])
        
        if not arg in DatasetState.STATES:
            err_msg = 'Parameter value [%s] is not a valid dataset state!' % (arg)
            raise DQInvalidRequestException(err_msg)


def is_date (args):
    """
    Tests if the given date is valid.
    
    @since: 0.3.0
    
    @param args: is the list of arguments to be tested.
    
    B{Exceptions}
        - DQInvalidRequestException is raised,
            in case date is not a string,
            doesn't match the regular expression (dq2.common.validator.DATE_REGEXP).
    
    Regular expressions documentation can be found at:
        http://www.amk.ca/python/howto/regex/
        http://docs.python.org/lib/module-re.html
    """
    
    for arg in args:
        is_string([arg])
        
        if len(arg) <= 0 or len(arg) > 19:
            err_msg = 'Parameter length [%s](%u) should be 18!' % (arg, len(arg))
            raise DQInvalidRequestException(err_msg)
            
        if DATE_COMPILED_REGEXP.match(arg, 0) is None:
            err_msg = 'Parameter value [%s] is not a valid date (%s)!' % (arg, DATE_REGEXP)
            raise DQInvalidRequestException(err_msg)
            
        tmp = arg.split(' ')
        tmp_date = tmp[0].split('-')
        
        if len(tmp) == 2:
            """has a date and time part"""
            tmp_time = tmp[1].split(':')
            try:
                datetime.datetime(
                    int(tmp_date[0]),
                    int(tmp_date[1]),
                    int(tmp_date[2]),
                    int(tmp_time[0]),
                    int(tmp_time[1]),
                    int(tmp_time[2])
                )
            except ValueError as e:
                err_msg = 'Parameter value [%s] is not a valid date (%s)!' % (arg, str(e))
                raise DQInvalidRequestException(err_msg)
            except ImportError:
                pass
        else:
            """only has a date part"""
            try:
                datetime.datetime(
                    int(tmp_date[0]),
                    int(tmp_date[1]),
                    int(tmp_date[2])
                )
            except ValueError as e:
                err_msg = 'Parameter value [%s] is not a valid date (%s)!' % (arg, str(e))
                raise DQInvalidRequestException(err_msg)
            except ImportError:
                pass

def is_datetime (args):
    """
    Tests if the given datetime is valid.
    
    @since: 0.3.0
    
    @param args: is the list of arguments to be tested.
    
    B{Exceptions}
        - DQInvalidRequestException is raised,
            in case datetime is not a string,
            doesn't match the regular expression.
    
    """
    for arg in args:
        try:
            pass
        except ValueError as e:
            err_msg = 'Parameter value [%s] is not a valid datetime (%s)!' % (arg, str(e))
            raise DQInvalidRequestException(err_msg)        
    return True


def is_timedelta (args):
    """
    Tests if the given timedelta is valid.
    
    @since: 0.3.0
    
    @param args: is the list of arguments to be tested.
    
    B{Exceptions}
        - DQInvalidRequestException is raised,
            in case timedelta is not a string,
            doesn't match the regular expression.
    
    """
    
    timedeltas = list ()
    for arg in args:
        is_string([arg])
                
        try:
            d = re.match(
                    r'((?P<days>\d+) days?)?'
                    r'(, )?'
                    r'((?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d+))?'
                    , str(arg))
            
            if not filter (lambda r: r[1], d.groupdict().items()):
                err_msg = 'Parameter value [%(arg)s] is not a valid time delta !' % locals ()
                raise DQInvalidRequestException(err_msg)                
                
            delta = datetime.timedelta (**dict ([ (key, (value and int(value) or 0)) for key, value in d.groupdict(0).items()]))
            timedeltas.append (delta)        
        except:
                err_msg = 'Parameter value [%(arg)s] is not a valid time delta !' % locals ()
                raise DQInvalidRequestException(err_msg)
                    
    return timedeltas 

def is_date_criteria (args):
    """
    Tests if the given criteria is a valid date filter criteria.
    
    @since: 0.3.0
    
    @param args: is the list of arguments to be tested.
    
    B{Exceptions}
        - DQInvalidRequestException is raised,
            in case the given attribute is not a valid metadata attribute.
    """
    
    for arg in args:
        is_string([arg])
        
        if not arg in DateCriteria.__ALL__:
            err_msg = 'Parameter [%s] is not a valid date criteria!' % (arg)
            raise DQInvalidRequestException(err_msg)


def is_dictionary (args):
    """
    Make sure all args are dictionaries, if not throw an exception.
    
    @since: 0.2.3
    
    @param args: is the list of arguments to be tested.
    
    B{Exceptions}
        - DQInvalidRequestException is raised,
            in case, at least, one of the arguments is not a list.
    """
    
    for arg in args:
        if not isinstance(arg, dict):
            err_msg = '%s is not a dictionary!' % (str(arg))
            raise DQInvalidRequestException(err_msg)


def is_filesize (arg):
    """
    Make sure all argument is a number and bigger than zero.
    
    @since: 1.1
    
    @param arg: the argument to be tested.
    
    B{Exceptions}
        - DQInvalidRequestException is raised,
            in case, at least, the given argument: is not a number or is zero.
    """
    
    if not isinstance(arg, int) and not isinstance(arg, long):
        """not an int"""
        err_msg = '%s is not an int!' % (str(arg))
        raise DQInvalidRequestException(err_msg)
    elif arg == 0:
        err_msg = 'File size cannot be zero!'
        raise DQInvalidRequestException(err_msg)


def is_http_url (args):
    """
    Tests if the given url is a valid URL
    (in the form of http://<host>:<port>/
    NOT in the form of http://<host>:<port>/<path>?<searchpart>
    as described in RFC1738).
    @since: 0.2.1
    
    @param args: is the list of arguments to be tested.
    
    B{Exceptions}
        - DQInvalidRequestException is raised,
            in case url is not a string or if it
            doesn't match the regular expression (dq2.common.validator.URL_REGEXP).
    
    URL documentation can be found at:
    http://www.cse.ohio-state.edu/cs/Services/rfc/rfc-text/rfc1738.txt
    (section 3.3 HTTP)
    """
    
    for arg in args:
        is_string([arg])
        
        if URL_COMPILED_REGEXP.match(arg, 0) is None:
            err_msg = 'Parameter value [%s] is not a valid URL (%s)!' % (arg, URL_REGEXP)
            raise DQInvalidRequestException(err_msg)


def is_integer (args):
    """
    Make sure all args are ints, if not throw an exception.
    
    @since: 0.2.0
    
    @param args: is the list of arguments to be tested.
    
    B{Exceptions}
        - DQInvalidRequestException is raised,
            in case, at least, one of the arguments is not an integer.
    """
    
    for arg in args:
        if not isinstance(arg, int):
            err_msg = '%s is not an int!' % (str(arg))
            raise DQInvalidRequestException(err_msg)


def is_lfn (args):
    """
    Tests if the given parameter is a valid logical filename.
    
    @since: 0.2.8
    
    @param args: is the list of arguments to be tested.
    
    B{Exceptions}
        - DQInvalidRequestException is raised,
            in case lfn is not a string or
            exceeds the maximum length (dq2.common.constants.LFN_MAXLENGTH).
    
    Regular expressions documentation can be found at:
    http://www.amk.ca/python/howto/regex/
    http://docs.python.org/lib/module-re.html
    """
    
    for arg in args:
        is_string([arg])
        
        if len(arg) == 0:
            err_msg = 'Parameter value [%s] length is zero!' % (arg)
            raise DQInvalidRequestException(err_msg)
        
        if len(arg) > LFN_MAXLENGTH:
            err_msg = 'Parameter value [%s] exceeds the maximum length (%u)!' % (arg, LFN_MAXLENGTH)
            raise DQInvalidRequestException(err_msg)
        
        has_no_blank_spaces([arg])
        has_characters([arg], ['\\', '/', '@'])


def is_list (args):
    """
    Make sure all args are lists, if not throw an exception.
    
    @since: 0.2.3
    
    @param args: is the list of arguments to be tested.
    
    B{Exceptions}
        - DQInvalidRequestException is raised,
            in case, at least, one of the arguments is not a list.
    """
    
    for arg in args:
        if not isinstance(arg, list):
            err_msg = '%s is not a list! (%s)' % (str(arg), str(type(arg)))
            raise DQInvalidRequestException(err_msg)


def is_long (args):
    """
    Make sure all args are ints, if not throw an exception.
    
    @since: 0.2.0
    
    @param args: is the list of arguments to be tested.
    
    B{Exceptions}
        - DQInvalidRequestException is raised,
            in case, at least, one of the arguments is not an integer.
    """
    
    for arg in args:
        if not isinstance(arg, long):
            err_msg = '%s is not a long!' % (str(arg))
            raise DQInvalidRequestException(err_msg)


def is_md5 (args):
    """
    Tests if the given checksum is a valid checksum supporting both MD5 and ADLER32.
    
    @since: 0.3.0
    
    @param args: is the list of arguments to be tested.
    
    B{Exceptions}
        - DQInvalidRequestException is raised,
            in case uid is not a string,
            doesn't match the regular expression (dq2.common.validator.ADLER32_REGEXP
            or dq2.common.validator.MD5_REGEXP).
    
    Regular expressions documentation can be found at:
    http://www.amk.ca/python/howto/regex/
    http://docs.python.org/lib/module-re.html
    """
    
    for arg in args:
        is_string([arg])
        
        if len(arg) > MD5_MAXLENGTH:
            err_msg = 'Parameter value [%s] exceeds the maximum length (%u)!' % (arg, MD5_MAXLENGTH)
            raise DQInvalidRequestException(err_msg)
        
        if MD5_COMPILED_REGEXP.match(arg, 0) is None and ADLER32_COMPILED_REGEXP.match(arg, 0) is None:
            err_msg = 'Parameter value [%s] is not a valid adler32/md5 checksum (%s : %s)!' % (arg, ADLER32_REGEXP, MD5_REGEXP)
            raise DQInvalidRequestException(err_msg)


"""
As of version 0.3.3, both MD5 and ADLER32 are supported. For compatibility purposes
the is_md5(...) supports both checksum types directly. In the future this support
will be split into two methods. For the sake of naming consistency, an alias
is_checksum(...) is implemented, which is what should be used from now on when
both checksum types should be accepted. 
"""
is_checksum = is_md5


def is_metadata_attribute (args):
    """
    Tests if the given attribute is a valid metadata attribute.
    
    @since: 0.2.9
    
    @param args: is the list of arguments to be tested.
    
    B{Exceptions}
        - DQInvalidRequestException is raised,
            in case the given attribute is not a valid metadata attribute.
    """
    
    for arg in args:
        is_string([arg])
        
        if not arg in Metadata.DATASET and not arg in Metadata.DATASET_VERSION \
            and not arg in Metadata.USER_VERSION and not arg in Metadata.USER_DATASET:
            err_msg = 'Parameter [%s] is not a valid metadata attribute!' % (arg)
            raise DQInvalidRequestException(err_msg)


def is_number (args):
    """
    Make sure all args are numbers, if not throw an exception.
    
    @since: 0.2.11
    
    @param args: is the list of arguments to be tested.
    
    B{Exceptions}
        - DQInvalidRequestException is raised,
            in case, at least, one of the arguments is not an integer.
    """
    
    for arg in args:
        if not isinstance(arg, int) and not isinstance(arg, float) and not isinstance(arg, long):
            err_msg = '%s is not a number!' % (str(arg))
            raise DQInvalidRequestException(err_msg)


def is_owner (args):
    """
    Make sure argument is string and have the ...
    
    @since: 0.3.0
    
    @param args: is the list of arguments to be tested.
    
    B{Exceptions}
        - DQInvalidRequestException is raised,
            in case, the argument is not a valid owner.
    """
    
    for arg in args:
        is_string([arg])
        
        if arg.find('CN') < 0:
            err_msg = '%s is not a valid DN!' % (arg)
            raise DQInvalidRequestException(err_msg)


def is_pfn (args):
    """
    Tests if the given parameter is a valid physical filename.
    
    @since: 0.3.0
    
    @param args: is the list of arguments to be tested.
    
    B{Exceptions}
        - DQInvalidRequestException is raised,
            in case pfn is not a string or
            exceeds the maximum length (dq2.common.constants.PFN_MAXLENGTH).
    
    Regular expressions documentation can be found at:
    http://www.amk.ca/python/howto/regex/
    http://docs.python.org/lib/module-re.html
    """
    
    for arg in args:
        is_string([arg])
        
        if len(arg) == 0:
            err_msg = 'Parameter value [%s] length is zero!' % (arg)
            raise DQInvalidRequestException(err_msg)
        
        if len(arg) > PFN_MAXLENGTH:
            err_msg = 'Parameter value [%s] exceeds the maximum length (%u)!' % (arg, PFN_MAXLENGTH)
            raise DQInvalidRequestException(err_msg)
        
        has_no_blank_spaces([arg])
        has_characters([arg], ['\\', '@'])


def is_string (args):
    """
    Make sure all args are strings, if not throw an exception.
    
    @since: 0.3.0
    
    @param args: is the list of arguments to be tested.
    
    B{Exceptions}
        - DQInvalidRequestException is raised,
            in case, at least, one of the arguments is not a string.
    """
    
    for arg in args:
        if not isinstance(arg, basestring):
            err_msg = '%s is not a string!' % (str(arg))
            raise DQInvalidRequestException(err_msg)


def is_tuple (args):
    """
    Make sure all args are tuples, if not throw an exception.
    
    @since: 0.2.10
    
    @param args: is the list of arguments to be tested.
    
    B{Exceptions}
        - DQInvalidRequestException is raised,
            in case, at least, one of the arguments is not a tuple.
    """
    
    for arg in args:
        if not isinstance(arg, tuple):
            err_msg = '%s is not a tuple!' % (str(arg))
            raise DQInvalidRequestException(err_msg)


def is_uid (args):
    """
    Tests if the given uid is a valid generated UUID.
    
    @since: 0.2.1
    
    @param args: is the list of arguments to be tested.
    
    B{Exceptions}
        - DQInvalidRequestException is raised,
            in case uid is not a string,
            exceeds the maximum length (dq2.common.constants.UID_MAXLENGTH) or
            doesn't match the regular expression (dq2.common.validator.UID_REGEXP).
    
    Regular expressions documentation can be found at:
    http://www.amk.ca/python/howto/regex/
    http://docs.python.org/lib/module-re.html
    """
    
    for arg in args:
        is_string([arg])
        
        if len(arg) > UID_MAXLENGTH:
            err_msg = 'Parameter value [%s] exceeds the maximum length (%u)!' % (arg, UID_MAXLENGTH)
            raise DQInvalidRequestException(err_msg)
        
        if UID_COMPILED_REGEXP.match(arg, 0) is None:
            err_msg = 'Parameter value [%s] is not a valid uid! UID should have the following format: %s' % (arg, UID_REGEXP)
            raise DQInvalidRequestException(err_msg)


def is_uid_lfn_dict (arg):
    """
    Tests the argument is a dictionary of uids mapped to LFNs.

    @since: 0.3.0

    @param args: is the list of arguments to be tested.

    B{Exceptions}
        - DQInvalidRequestException is raised,
          if any of the is_uid or is_lfn tests fail
    """

    is_dictionary([arg])

    for key, value in arg.items():
        is_uid([key])
        is_lfn([value])


def not_all_none (arg):
    """
    Tests at least one of the items in arg is not None.

    @since: 0.3.0

    @param args: is a list of items to test

    B{Exceptions}
        - DQInvalidRequestException is raised,
        if all the items in arg are None or arg is not a list.

    """

    is_list([arg])
    for item in arg:
        if item is not None:
            return

    err_msg = 'At least one argument must not be None!'
    raise DQInvalidRequestException(err_msg)
