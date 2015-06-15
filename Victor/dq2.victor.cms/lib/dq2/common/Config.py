"""
Cache for the configuration file sections and attributes.

@author: Pedro Salgado
@contact: pedro.salgado@cern.ch
@since: 1.2.0
@version: $Id: Config.py,v 1.15 2010-10-04 13:24:07 vgaronne Exp $
"""

__package__ = __name__
__version__ = '$Revision: 1.15 $'
# $Source: /tmp/dq2svn/cvs/cvs/dq2.common/lib/dq2/common/Config.py,v $


import os
import threading

try:
    from ConfigParser import SafeConfigParser as ConfigParser_
except:
    # python 2.2
    from ConfigParser import ConfigParser as ConfigParser_
from ConfigParser import NoSectionError, ParsingError

from dq2.common.DQException import DQConfigurationException


class Config (object):
    """
    Class definition for a dq2 Config object.
    
    Current version looks for the config file in ''.
    
    @author: Ricardo Rocha
    @contact: ricardo.rocha@cern.ch
    @version: $Revision: 1.15 $
    
    @cvar _configs: service configuration objects.
    @type _configs: dict
    @cvar _instance: holds the singleton reference.
    @type _instance: Config
    """


    _configs = {}
    _instance = None


    def __new__ (cls):
        """
        Invoked on every class instance creation.
        
        Makes sure that only one instance of this class ever exists.
        
        @return: A reference to the class singleton
        """
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance


    def __init__ (self):
        """
        Object constructor.
        
        As this is a singleton, nothing is put in here (otherwise it would
        be constantly called).
        """
        pass


    def getConfig (self, packageName, mypath=None):
        """
        Returns a reference to the configuration object for the given package.
        
        @param packageName: The name of the package for which to retrieve the configuration
        @type packageName: .
        @keyword mypath: an alternative path to search for a configuration file.
        @type mypath: str
        
        @change: the 'mypath' parameter was added to the original problem.
        
        @return: A reference to the config object of the requested package
        """
        # return the config immediately if we already have one for this package
        if not self._configs.has_key(packageName):
            
            # else load it and return afterwards
            if mypath is not None:
                configFiles = [
                    '/opt/dq2/etc/dq2.cfg',
                    '/opt/dq2/etc/%s/%s.cfg' % (packageName, packageName),
                    os.path.expanduser('~/.dq2/etc/dq2.cfg'),
                    os.path.expanduser('~/.dq2/etc/%s/%s.cfg' % (packageName, packageName)),
                    '%s/etc/dq2.cfg' % os.environ.get('DQ2_HOME'),
                    '%s/etc/%s/%s.cfg' % (os.environ.get('DQ2_HOME'), packageName, packageName),
                    mypath + '/etc/dq2.cfg',
                    mypath + '/etc/%s/%s.cfg' % (packageName, packageName)
                ]
            else:
                configFiles = [
                    '/opt/dq2/etc/dq2.cfg',
                    '/opt/dq2/etc/%s/%s.cfg' % (packageName, packageName),
                    os.path.expanduser('~/.dq2/etc/dq2.cfg'),
                    os.path.expanduser('~/.dq2/etc/%s/%s.cfg' % (packageName, packageName)),
                    '%s/etc/dq2.cfg' % os.environ.get('DQ2_HOME'),
                    '%s/etc/%s/%s.cfg' % (os.environ.get('DQ2_HOME'), packageName, packageName)
                ]
            
            config = ConfigParser_()
            
            try:
                config.read(configFiles)
                self._configs[packageName] = config
            except ParsingError as msg:
                # @todo: we need to log the exception somewhere
                # problem is without loading the config we have no logger
                return None
        
        return self._configs[packageName]

    def resetConfig (self, packageName):
        """
        Removes the cached configuration for this package.
        
        @since: 1.1.13
        
        @param packageName: The name of the package for which to retrieve the configuration
        @type packageName: str
        """
        del self._configs[packageName]


_CONFIGURATIONS = {}
_LOADED = {}
_LOCK = threading.Lock()


def _load_configuration (aDir, configurationSection):
    """
    Tries to load the configuration for the given section, on the given directory.
    
    First, it will try to load the configuration from aDir/etc/dq2.cfg;
    otherwise it will try the aDir/etc/configurationSection/configurationSection.cfg file instead.
    
    @since: 1.2.0
    
    @param aDir: the name of the directory to retrieve the configuration.
    @type aDir: str
    @param configurationSection: the name of the section inside the configuration file.
    @type configurationSection: str
    
    @raise ValueError:
        in case the given configuration section is None.
    @raise DQConfigurationException:
        in case there is no configuration file containing this section.
    
    @warning: this method is not thread-safe.
    
    @return: True if the configuration for this section was loaded; False otherwise.
    @rtype: bool
    """
    
    if configurationSection is None:
        raise ValueError('To retrieve the configuration of a section, its name cannot be None!')
    
    if aDir is None:
        return False
    
    config = ConfigParser_()
    
    # dq2.cfg
    f = ''.join((aDir, '/etc/dq2.cfg'))
    if not _LOADED.has_key(f):
        try:
            config.read(f)
            _LOADED[f] = None # file was successfully loaded
            # for dq2.cfg you must load all new sections
            for section in config.sections():
                if not _CONFIGURATIONS.has_key(section):
                    _CONFIGURATIONS[section] = {}
                    for k, v in (section):
                        _CONFIGURATIONS[section][k] = v
            
            if config.has_section(configurationSection):
                return True
        except (NoSectionError, ParsingError) as e:
            _LOADED[f] = str(e) # don't load again and store exception message
    
    # configurationSection/configurationSection.cfg
    f = ''.join((aDir, '/etc/', configurationSection, '/', configurationSection,'.cfg'))
    if not _LOADED.has_key(f):
        try:
            config.read(f)
            _LOADED[f] = None # file was successfully loaded
            # for configurationSection.cfg you must only load the [configurationSection] part
            if config.has_section(configurationSection):
                for k, v in config.items(configurationSection):
                    _CONFIGURATIONS[configurationSection][k] = v
            return config.has_section(configurationSection)
        except (NoSectionError, ParsingError) as e:
            _LOADED[f] = str(e) # don't load again and store exception message
    
    return False

def _load_section (configurationSection, mypath=None):
    """
    Loads a configuration section from dq2.cfg or configurationSection.cfg,
    in a thread-safe way.
    
    The directories to search for these configuration files are scanned in the following order:
    - the given path
    - DQ2_HOME environment variable
    - ~/.dq2
    - /opt/dq2
    
    The files to read the configuration information are scanned in the following order:
    - dq2.cfg
    - configurationSection/configurationSection.cfg
    
    @since: 1.2.0
    
    @param configurationSection: The name of the section to retrieve the configuration.
    @type configurationSection: str
    @keyword mypath: an alternative path to search for a configuration file.
    @type mypath: str
    
    @raise ValueError:
        in case the given configuration section is None.
    @raise DQConfigurationException:
        in case there is no configuration file containing this section.
    """
    
    if configurationSection is None:
        raise ValueError('To retrieve the configuration of a package, its name cannot be None!')
    
    _LOCK.acquire()
    
    try:
        if mypath is not None and _load_configuration(mypath, configurationSection):
            """given path"""
            return True
        else:
            if _load_configuration(os.environ.get('DQ2_HOME'), configurationSection):
                return
            elif _load_configuration(os.path.expanduser('~/.dq2'), configurationSection):
                return
            elif _load_configuration('/opt/dq2', configurationSection):
                return
    finally:
        _LOCK.release()
    
    # no configuration was found
    raise DQConfigurationException('Cannot find configuration for package %s!' % (configurationSection))

def get_section (configurationSection):
    """
    Retrieve the configuration attributes of a given section.
    
    @since: 1.2.0
    
    @param configurationSection: The name of the section to retrieve the configuration.
    @type configurationSection: str
    
    @raise ValueError:
        in case the given configuration section is None.
    @raise DQConfigurationException:
        in case there is no configuration file containing this section.
    """
    if configurationSection is None:
        raise ValueError('To retrieve the configuration of a package, its name cannot be None!')
    
    if not _CONFIGURATIONS.has_section(configurationSection):
        _load_section(configurationSection)
    return _CONFIGURATIONS[configurationSection]

def reset_section (configurationSection):
    """
    Removes the cached configuration for this section.
    
    @since: 1.2.0
    
    @param configurationSection: The name of the section for which to retrieve the configuration.
    @type configurationSection: str
    """
    del _CONFIGURATIONS[configurationSection]
    _LOADED = {} # to reload the section from previously loaded files