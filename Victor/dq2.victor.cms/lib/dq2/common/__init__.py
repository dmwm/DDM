"""
Package contains all modules for the DQ2 common component.

@author: David Cameron
@contact: david.cameron@cern.ch
@author: Miguel Branco
@contact: miguel.branco@cern.ch
@author: Pedro Salgado
@contact: pedro.salgado@cern.ch
@since: 0.3.0
@version: $Id: __init__.py,v 1.32 2010-10-04 13:24:09 vgaronne Exp $
"""

__package__ = __name__
__version__ = '$Revision: 1.32 $'
# $Source: /tmp/dq2svn/cvs/cvs/dq2.common/lib/dq2/common/__init__.py,v $


import commands
import re
import string
import threading


from dq2.common.DQException import DQFatalError
try:
    """try to get uuid module from python distribution"""
    import uuid
except:
    """not there"""
    try:
        from dq2.common.python import uuid
    except:
        """ctypes sometimes is missing as well!"""
        pass


def generate_uuid ():
   """
   Generates a fixed 36 character unique identifier (in lowercase).
   
   @author: Miguel Branco
   @contact: miguel.branco@cern.ch
   @since: 0.2.0
   @version: $Id: __init__.py,v 1.32 2010-10-04 13:24:09 vgaronne Exp $
   
   @raise DQFatalError: in case there is an error running uuidgen.
   
   @return: a 36 character unique identifier.
   @rtype: str
   """
   try:
       return str(uuid.uuid4()).lower()
   except:
       """python 2.2 compatibility"""
       s,o = commands.getstatusoutput('uuidgen')
       if s != 0:
           err_msg = 'Failed running uuidgen to generate UUID! [%s]' % (o)
           raise DQFatalError(err_msg)
       return string.strip(o).lower()


def generate_timed_uuid ():
    """
    """
    try:
       return str(uuid.uuid1()).lower()
    except:
       """python 2.2 compatibility"""
       s,o = commands.getstatusoutput('uuidgen -t')
       if s != 0:
           s,o = commands.getstatusoutput('uuidgen')
           if s != 0:
               err_msg = 'Failed running uuidgen to generate UUID! [%s]' % (o)
               raise DQFatalError(err_msg)
       return string.strip(o).lower()


def dict_get_item (dictionary, key):
    """
    Returns a value from a dictionary in a case-insensitive way.
    
    @since: 0.2.0
    
    @param dictionary: the dictionary from where to retrieve the value.
    @type dictionary: dict
    @param key: the dictionary key.
    @type key: unknown
    
    @raise AssertionError: in case the dictionary is None.
    @raise AssertionError: in case the dictionary parameter is not a dictionary.
    @raise AssertionError: in case the key of the dictionary is None.
    @raise KeyError: in case the key cannot be found in the dictionary.
    """
    assert dictionary is not None
    assert isinstance(dictionary, dict)
    assert key is not None
    
    for eachKey in dictionary.keys():
        """"""
        if eachKey.lower() == key.lower():
            return dictionary[eachKey]
    
    raise KeyError

get_dict_item = dict_get_item


def get_hostname (url):
    """
    Return hostname from URL.
    
    @since: 0.2.0
    
    @param url: the URL to be parsed.
    @type url: str
    
    @return: the hostname.
    @rtype: str
    """
    reg = re.search('[^:]+:(/)*([^:/]+)(:[0-9]+)?(/)?.*', url)
    host = ''
    try:
        host = reg.group(2)
    except:
        pass
    
    return host


def parse_dn (owner):
    """
    @since: 0.3.0
    
    @param owner: the certificate DN.
    @type owner: str
    
    @return: a parsed certificate DN.
    @rtype: str
    """
    if owner is not None:
        owner = owner.split('/CN=')
        if len(owner) >= 2:
            owner = owner[0] + '/CN=' + owner[1]
        else:
            owner = owner[0]
    return owner


def time_uuid (uuid_time):
    """
    @author: Pedro Salgado
    @contact: pedro.salgado@cern.ch
    @param uuid_time: the time of the uuid. it can be retrieved by using generated_uuid.get_time().
    """
    uuid_time -= 122192928000000000L
    # and convert to milliseconds as the system clock is in millis
    uuid_time /= 10000L * 1000
    
    return uuid_time


def uuid_at_timestamp (date):
    """
    @author: Pedro Salgado
    @contact: pedro.salgado@cern.ch
    
    Example:
        
        >>> dateDt = datetime.datetime(year=2007, month=1, day=1)
        >>> dateDt.ctime()
        'Mon Jan  1 00:00:00 2007'
        >>> uuid = uuid_at_timestamp(calendar.timegm(dateDt.timetuple()))
        >>> time.ctime(time_uuid(uuid.get_time()))
        'Mon Jan  1 00:00:00 2007'
    """
    import time
    nanoseconds = int(date * 1e9)
    # 0x01b21dd213814000 is the number of 100-ns intervals between the
    # UUID epoch 1582-10-15 00:00:00 and the Unix epoch 1970-01-01 00:00:00.
    timestamp = int(nanoseconds/100) + 0x01b21dd213814000L
    
    import random
    clock_seq = random.randrange(1<<14L) # instead of stable storage
    
    time_low = timestamp & 0xffffffffL
    time_mid = (timestamp >> 32L) & 0xffffL
    time_hi_version = (timestamp >> 48L) & 0x0fffL
    
    clock_seq_low = clock_seq & 0xffL
    clock_seq_hi_variant = (clock_seq >> 8L) & 0x3fL
    
    node = getnode()
    
    return UUID(fields=(time_low, time_mid, time_hi_version,
                    clock_seq_hi_variant, clock_seq_low, node), version=1)


class Singleton (object):
    """
    Class to be used to create singleton classes.
    
    @author: Pedro Salgado
    @contact: pedro.salgado@cern.ch
    @since: 0.3.0
    @version: $Revision: 1.32 $
    """


    def __new__ (cls, *args, **kwds):
        """
        @since: 0.3.0
        
        @return: the singleton.
        @rtype: object
        """
        
        instance = cls.__dict__.get('__instance__')
        if instance is not None:
            return instance
        cls.__instance__ = instance = object.__new__(cls)
        instance.init(*args, **kwds)
        return instance


    def init (self, *args, **kwds):
        """
        Method to be implemented by the subclasses.
        
        @since: 0.3.0
        """
        pass


class Configurable (object):
    """
    Class to be used to create configurable classes.
    
    @author: Pedro Salgado
    @contact: pedro.salgado@cern.ch
    @since: 0.3.0
    @version: $Revision: 1.32 $
    
    @cvar isConfigured: flag to determine if a class has been configured or not.
    @type isConfigured: bool
    @cvar lock: a lock to safely configure the class.
    @type lock: threading.Lock
    """


    isConfigured = False
    lock = threading.Lock()


    def __new__ (cls, *args, **kwds):
        """
        @since: 0.3.0
        """
        # get the subclass configured attribute
        try:
            isConfigured = cls.__dict__.get('isConfigured')
        except AttributeError as e:
            setattr(cls, 'isConfigured', False)
            
        if cls.isConfigured is None or cls.isConfigured is False:
            """no configuration present (yet) - if it was it would skip the lock -> more performant"""
            
            #LOCK: begin
            Configurable.lock.acquire()
            
            try:
                # a previous thread may had the lock and configured the class
                # need to verify again
                
                if not cls.isConfigured is True:
                    """still not configured"""
                    #print 'configuring %s...' % cls
                    cls.__configure__()
                    cls.isConfigured = True
            finally:
                Configurable.lock.release()
            #LOCK: end
        
        return super(Configurable, cls).__new__(cls)


    def __configure__ ():
        """
        Method to be implemented by the subclasses.
        
        @since: 0.3.0
        """
        pass

    __configure__ = staticmethod(__configure__)


import new
from types import MethodType


class Proxy (object):
    """
    @see: http://www.python.org/workshops/1997-10/proceedings/savikko.html
    @see: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/519639
    """


    def __init__ (self, subject):
        """
        """
        self.__subject = subject


    def __getattr__(self, aname):
        target = self.__subject
        f = getattr(target, aname)
        if isinstance(f, MethodType):
            # Rebind the method to the target.
            return new.instancemethod(f.im_func, self, target.__class__)
        else:
            return f


    def __subject():
        """
        """
        return self.__subject