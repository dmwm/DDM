"""


@author: Miguel Branco
@contact: miguel.branco@cern.ch
@since: 0.3.0
@version: $Id: DQDashboardTool.py,v 1.1 2008-05-29 11:15:39 psalgado Exp $
"""


from dq2.common import log as logging
from dq2.common.Config import Config
from dq2.common.optparse import OptionParser


class DQDashboardTool:
    """
    @since: 0.3.0
    
    @cvar defaultOptions: overwritten default set of options that apply to all the CLI tools.
    @type defaultOptions: list
    @cvar defaultQueryOptions: .
    @type defaultQueryOptions: list
    @cvar package: .
    @type package: str
    @cvar remoteOptions: .
    @type remoteOptions: list
    @cvar version: DQ2 own version.
    @type version: str
    """
    
    defaultOptions = []
    defaultQueryOptions = []
    package = None
    remoteOptions = []
    version = '$Revision 0.3 $'


    def __init__ (self, query=False, remote=False):
        """
        Class constructor.
        
        @author: Miguel Branco
        @contact: miguel.branco@cern.ch
        @since: 0.3
        @version: $Id: DQDashboardTool.py,v 1.1 2008-05-29 11:15:39 psalgado Exp $
        
        @param query: Boolean indicating if default query options are available
            or not
        @param remote: Boolean indicating if default remote access (service, port)
            options are available or not
        """
        self.__class__._logger = logging.getLogger(self.__module__)
            
        self.parser = OptionParser(usage=self.usage, version=self.version,
                                   description=self.description)
        
        # default options are always available
        options = self.defaultOptions
        # if this is a 'query' tool, default query options are available
        if query:
            options.extend(self.defaultQueryOptions)
        # if this is a 'remote access' tool, service, port and alike options
        # are also available
        if remote:
            options.extend(self.remoteOptions)
        # finally, tool specific options should be added
        options.extend(self.toolOptions)
        
        # add all the options to the parser
        for option in options:
            self.parser.add_option(option)
        
        # parse the command line arguments and options and update the options
        (self.options, self.args) = self.parser.parse_args()


# PRIVATE methods


    def _get_parameters (self):
        """
        Abstract method to be implemented in subclasses if needed.
        
        @since: 0.3.0
        """
        pass