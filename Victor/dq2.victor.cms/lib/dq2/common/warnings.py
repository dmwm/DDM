"""


@author: Pedro Salgado
@contact: pedro.salgado@cern.ch
@since: 1.0
@version: $Id: warnings.py,v 1.1 2008-05-29 11:16:15 psalgado Exp $
"""


from dq2.common.DQException import DQException, DQUserError, DQWarning


class ElementNotInContainer (DQException, DQUserError, DQWarning):
    """
    Warning class for the cases when a container does not contain a given element.
    
    @author: Pedro Salgado
    @contact: pedro.salgado@cern.ch
    @since: 1.0
    @version: $Revision: 1.1 $
    """


    def __init__ (self, name, dsn, version):
        """
        @since: 1.0
        
        @param name: name of the container.
        @type name: str
        @param dsn: dataset name.
        @type dsn: str
        @param version: dataset version.
        @type version: int
        
        """
        self.name = name
        self.dsn = dsn
        if version is not None:
            self.version = version
        else:
            self.version = ''
        DQException.__init__(self)


    def __str__ (self):
        """
        Returns a string representation of this object.
        
        @since: 1.0
        """
        message = 'The container %s does not contain %s %s!' % (self.name, self.dsn, self.version)
        return '%s%s %s' % (DQUserError.prefix, DQWarning.prefix, message)


class ContainerHasDatasetOfElement (DQException, DQUserError, DQWarning):
    """
    Warning class for the cases when a container already contains a dataset of the element being registered.
    
    @author: Pedro Salgado
    @contact: pedro.salgado@cern.ch
    @since: 1.0
    @version: $Revision: 1.1 $
    """


    def __init__ (self, name, dsn, version):
        """
        @since: 1.0
        
        @param name: name of the container.
        @type name: str
        @param dsn: dataset unique name.
        @type dsn: str
        @param version: dataset version.
        @type version: int
        
        """
        self.name = name
        self.dsn = dsn
        self.version = version
        DQException.__init__(self)


    def __str__ (self):
        """
        Returns a string representation of this object.
        
        @since: 1.0
        """
        message = 'The container %s contains the dataset of the version %s %s!' % (self.name, self.dsn, self.version)
        return '%s%s %s' % (DQUserError.prefix, DQWarning.prefix, message)


class ContainerHasElement (DQException, DQUserError, DQWarning):
    """
    Warning class for the cases when a container already contains the given element.
    
    @author: Pedro Salgado
    @contact: pedro.salgado@cern.ch
    @since: 1.0
    @version: $Revision: 1.1 $
    """


    def __init__ (self, name, dsn, version):
        """
        @since: 1.0
        
        @param name: name of the container.
        @type name: str
        @param dsn: dataset name.
        @type dsn: str
        @param version: dataset version.
        @type version: int
        
        """
        self.name = name
        self.dsn = dsn
        if version is not None:
            self.version = version
        else:
            self.version = ''
        DQException.__init__(self)


    def __str__ (self):
        """
        Returns a string representation of this object.
        
        @since: 1.0
        """
        message = 'The container %s already contains %s %s!' % (self.name, self.dsn, self.version)
        return '%s%s %s' % (DQUserError.prefix, DQWarning.prefix, message)


class ContainerHasLowerVersion (DQException, DQUserError, DQWarning):
    """
    Warning class for the cases when a container already contains a lower version of the element being registered.
    
    @author: Pedro Salgado
    @contact: pedro.salgado@cern.ch
    @since: 1.0
    @version: $Revision: 1.1 $
    """


    def __init__ (self, name, dsn, version):
        """
        @since: 1.0
        
        @param name: name of the container.
        @type name: str
        @param dsn: dataset name.
        @type dsn: str
        @param version: dataset version.
        @type version: int
        
        """
        self.name = name
        self.dsn = dsn
        self.version = version
        DQException.__init__(self)


    def __str__ (self):
        """
        Returns a string representation of this object.
        
        @since: 1.0
        """
        message = 'The container %s had a previous version which was updated to %s version %s!' % (self.name, self.dsn, self.version)
        return '%s%s %s' % (DQUserError.prefix, DQWarning.prefix, message)


class ContainerHasHigherVersion (DQException, DQUserError, DQWarning):
    """
    Warning class for the cases when a container already contains a higher version of the element being registered.
    
    @author: Pedro Salgado
    @contact: pedro.salgado@cern.ch
    @since: 1.0
    @version: $Revision: 1.1 $
    """


    def __init__ (self, name, dsn, version):
        """
        @since: 1.0
        
        @param name: name of the container.
        @type name: str
        @param dsn: dataset name.
        @type dsn: str
        @param version: dataset version.
        @type version: int
        
        """
        self.name = name
        self.dsn = dsn
        self.version = version
        DQException.__init__(self)


    def __str__ (self):
        """
        Returns a string representation of this object.
        
        @since: 1.0
        """
        message = 'The container %s contains a higher dataset version of the dataset %s %s!' % (self.name, self.dsn, self.version)
        return '%s%s %s' % (DQUserError.prefix, DQWarning.prefix, message)