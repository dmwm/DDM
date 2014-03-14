"""
"8.2 State Guidelines
(...)
168. State Names Should Be Simple but Descriptive
(...)
Ideally, state names should also be written in present tense,
although names such as Proposed (past tense) are better than
Is Proposed (present tense).
", The Elements of UML Style - Scott W. Ambler

@var tag: the DQ2 tag.
@type tag: str
@deprecated: the tag variable has been copied to dq2.common.__version__.
"""


tag = '$Name: not supported by cvs2svn $'


API_030 = 30
API_100 = 100
APIS = [API_030, API_100]


class CallbackType:
    """
    (since 0.2.11)
    """
    DATASET_COMPLETE_EVENT       = 'DATASET_COMPLETE_EVENT'
    DATASET_BROKEN_EVENT         = 'DATASET_BROKEN_EVENT'    
    FILE_DONE_EVENT              = 'FILE_DONE_EVENT'
    FILES_ON_SITE_EVENT          = 'FILES_ON_SITE_EVENT'
    FILES_IN_DATASET_EVENT       = 'FILES_IN_DATASET_EVENT'
    SUBSCRIPTION_QUEUED_EVENT    = 'SUBSCRIPTION_QUEUED_EVENT'
    SUBSCRIPTION_CANCELLED_EVENT = 'SUBSCRIPTION_CANCELLED_EVENT'
    SUBSCRIPTION_IGNORED_EVENT   = 'SUBSCRIPTION_IGNORED_EVENT'
    FILES_CANCELLED_EVENT        = 'FILES_CANCELLED_EVENT'
    FILES_TRANSFER_EVENT         = 'FILES_TRANSFER_EVENT'
    ERROR_EVENT                  = 'ERROR_EVENT'
    
    __ALL__ = [DATASET_COMPLETE_EVENT, DATASET_BROKEN_EVENT,
               FILE_DONE_EVENT, FILES_ON_SITE_EVENT, FILES_IN_DATASET_EVENT,
               FILES_CANCELLED_EVENT, FILES_TRANSFER_EVENT,               
               SUBSCRIPTION_QUEUED_EVENT, SUBSCRIPTION_CANCELLED_EVENT, SUBSCRIPTION_IGNORED_EVENT,               
               ERROR_EVENT]


class Component:
    """
    Class to reference DQ2 components.
    
    @author: Pedro Salgado
    @contact: pedro.salgado@cern.ch
    @since: 1.0
    
    @var CLIENT: DQ2 client component.
    @type CLIENT: str
    @var CURL: curl component.
    @type CURL: str
    @var WEBSERVICE: DQ2 webservice component.
    @type WEBSERVICE: str
    @var DAO: DQ2 data access object.
    @type DAO: str
    @var DATABASE: database component.
    @type DATABASE: str
    """
    CLIENT = 'CLI'
    CURL = 'CURL'
    WEBSERVICE = 'WS'
    DAO = 'DAO'
    DATABASE = 'DB'


class DatasetState:
    """
    Class to reference dataset states.
    
    @since: 0.2.0
    @version: $Revision: 1.21 $
    
    @cvar CLOSED: constant for the dataset 'open' state.
    @type CLOSED: int
    @cvar FROZEN: constant for the dataset 'open' state.
    @type FROZEN: int
    @cvar DELETED: constant for the dataset 'open' state.
    @type DELETED: int
    @cvar OPEN: the constant for the dataset 'open' state.
    @type OPEN: int
    """
    CLOSED = 1
    FROZEN = 2
    DELETED = 3
    OPEN = 0
    
    STATES = [OPEN, CLOSED, FROZEN, DELETED]
    DESCRIPTION = ['open', 'closed', 'frozen', 'archived']

ContainerState = DatasetState


class DatasetType:
    """
    Class to reference data set types.
    
    @since: 1.0
    @version: $Id: constants.py,v 1.21 2010-10-04 13:24:10 vgaronne Exp $
    
    @cvar CONTAINER: constant for containers.
    @type CONTAINER: int
    @cvar DATASET: constant for data sets.
    @type DATASET: int
    @cvar MERGED: constant for merged data sets.
    @type MERGED: int
    """
    CONTAINER = 2
    DATASET = 1
    MERGED = 3
    
    TYPES = [DATASET, CONTAINER, MERGED]
    DESCRIPTION = [None, 'dataset', 'container', 'merged']


class DateCriteria:
    """
    Class to reference date criterias.
    
    @since: 0.3
    @version: $Revision: 1.21 $
    
    @cvar LEQ: constant for the 'less or equal' criteria.
    @type LEQ: str
    @cvar GEQ: constant for the 'greater or equal' criteria.
    @type GEQ: str
    @cvar __ALL__: all of date criteria constants.
    @type __ALL__: list
    @cvar __ARGS__: command line tool arguments to specify date criterias.
    @type __ARGS__: list
    """
    LEQ = 'leq'
    GEQ = 'geq'
    
    __ALL__ = [LEQ, GEQ]
    __ARGS__ = ['--leq', '--geq']


class FileState:
    """
    Class to reference file operations in the content catalog.
    
    @author: Pedro Salgado
    @contact: pedro.salgado@cern.ch
    @since: 0.3
    @version: $Revision: 1.21 $
    
    @cvar ADDED: constant to specify a file registration on a dataset version.
    @type ADDED: int
    @cvar DELETED: constant to specify a file deletion on a dataset version.
    @type DELETED: int
    @cvar HIDDEN: constant to completely remove a file from a dataset (unused).
    @type HIDDEN: int
    """

    HIDDEN = 0
    ADDED = 1
    DELETED = 2


class HTTP:
    """
    Class to reference HTTP methods and mandatory names for parameters and headers.
    
    @author: Pedro Salgado
    @contact: pedro.salgado@cern.ch
    @since: 0.2.0
    @version: $Revision: 1.21 $
    
    @cvar API: name of the api parameter.
    @type API: str
    @cvar DELETE: name of the HTTP DELETE method.
    @type DELETE: type
    @cvar GET: name of the HTTP GET method.
    @type GET: str
    @cvar POST: name of the HTTP POST method.
    @type POST: str
    @cvar PUT: name of the HTTP PUT method.
    @type PUT: str
    @cvar TUID: name of the tuid parameter.
    @type TUID: str
    @cvar USER_AGENT: the name of the User-Agent header.
    @type USER_AGENT: str
    """

    GET = 'GET'
    POST = 'POST'
    DELETE = 'DELETE'
    PUT = 'PUT'

    # assumes tag is of the form DQ2_x_y_z
    API = 'API'
    USER_AGENT = 'User-Agent: dqcurl %s' % (tag[11:-2].replace('_', '.'))

    TUID = 'TUID'


class Metadata:
    """
    Class to reference DQ2 specific metadata attributes.
    
    @author: Pedro Salgado
    @contact: pedro.salgado@cern.ch
    @since: 0.2.0
    @version: $Revision: 1.21 $
    
    @cvar DATASET: dataset metadata attributes.
    @type DATASET: list
    @cvar DATASET_VERSION: dataset version metadata attributes.
    @type DATASET_VERSION: list
    @cvar USER_DATASET: user dataset metadata attributes.
    @type USER_DATASET: list
    @cvar USER_VERSION: user dataset version metadata attributes.
    @type USER_VERSION: list
    
    @deprecated: DATASET_VERSION 'latestvuid' is deprecated.
    """

    DATASET = ['duid', 'state', 'owner', 'creationdate', 'latestversion', 'lastoperationdn', 
               'lastoperationip', 'closeddate', 'frozendate', 'deleteddate', 'type', 'lifetime', 
               'freezingdate', 'group', 'provenance', 'hidden', 'nbfiles', 'length']
    DATASET_VERSION = ['vuid', 'version', 'versioncreationdate', 'latestvuid']
    USER_DATASET = ['origin', 'physicsgroup', 'lifetime', 'temperature', '#replicas']
    USER_VERSION = ['tier0state', 'tier0type']


class Role:
    """
    DDM system role.
    
    @author: Pedro Salgado
    @contact: pedro.salgado@cern.ch
    @since: 0.3.0
    @version: $Revision: 1.21 $
    """
    
    ADMIN = 'ADMIN'
    PRODUCTION = 'PRODUCTION'
    USER = 'USER'


class SourceResolverPolicy:
    """
    (since 0.2.2)
    """
    LRC_LOOKUP = 0
    RELATIVE_SURL = 1


class SourcesPolicy:
    """
    @since: 0.2.0
    """
    ALL_SOURCES        = 000001
    KNOWN_SOURCES      = 000010
    CLOSE_SOURCES      = 000100
    COMPLETE_SOURCES   = 001000
    INCOMPLETE_SOURCES = 010000
    
    VALUES = [ALL_SOURCES, KNOWN_SOURCES, CLOSE_SOURCES, COMPLETE_SOURCES, INCOMPLETE_SOURCES]


class SubscriptionArchivedState:
    """
    
    @since: 0.2.0
    """
    __ANY__ = None
    ARCHIVE = 1
    UNARCHIVE = 0
    
    STATES = [UNARCHIVE, ARCHIVE]


class TestCaseData:
    """
    Class to reference data for test purposes.
    
    @since: 0.2.0
    @version: $Revision: 1.21 $
    
    @cvar CHECKSUMS: MD5 file checksums to be used for testing purposes.
    @type CHECKSUMS: list
    @cvar DSNS: dataset names to be used for testing purposes.
    @type DSNS: list
    @cvar GUIDS: global unique identifiers to be used for testing purposes.
    @type GUIDS: list
    @cvar LFNS: logical file names to be used for testing purposes.
    @type LFNS: list
    @cvar INVERTED_VUIDS: .
    @type INVERTED_VUIDS: list
    @cvar OWNERS: dataset owners to be used for testing purposes.
    @type OWNERS: list
    @cvar SIZES: file sizes to be used for testing purposes.
    @type SIZES: list
    @cvar VUIDS: dataset version unique identifiers to be used for testing purposes.
    @type VUIDS: list
    """
    DSNS = [
        'test.dq2.2008-01-14.lxplus225.cern.ch.c7d9ef07-c2b1-11dc-a3e7-000423d950b0',
        'test.dq2.2007-11-02.lxplus232.cern.ch.4bfcd18c-8963-11dc-8b3b-000423d990f4',
        'test.dq2.' + 'a' * (255-len('test.dq2.')), #0
        'test.dq2.2007-11-02.lxplus233.cern.ch.4bfcd18c-8963-11dc-8b3b-000423d990f4',
        'test.dq2.',
        'test.dq2.csc11.005025.J2_pythia_jetjet_NoISR-FSR-MI.evgen.EVNT.v11004205',
        'test.dq2.csc11.005025.J2_pythia_jetjet_NoISR_FSR_MI.evgen.EVNT.v11004206',
        'test.dq2.trig_misal_whatever' #5
    ]
    LFNS = [
        'test.dq2.lfn.00001.w+w-piupiutautaumumu._00001.tar.gz', #0
        'test.dq2.lfn.00001.w+w-piupiutautaumumu._00002.tar.gz',
        'test.dq2.lfn.00001.w+w-piupiutautaumumu._00003.tar.gz',
        'test.dq2.lfn.00002',
        'test.dq2.lfn.00003',
        'test.dq2.lfn.00004', #5
        'test.dq2.lfn.00005',
        'test.dq2.lfn.00006'
    ]
    GUIDS = [
        '00000000-c8dc-416c-b923-2c7f2c2f0400', #0
        '00000000-A6EC-4B36-91D6-10845288EA00',
        '00000000-1234-1234-1234-123456789000',
        '00000000-1234-1234-1234-123456789001',
        '00000000-1234-1234-1234-123456789002',
        '00000000-1234-1234-1234-123456789003', #5
        '00000000-1234-1234-1234-123456789004',
        '00000000-1234-1234-1234-123456789005',
        '00000000-1234-1234-1234-123456789006'
    ]
    SIZES = [
        long(1000), long(2000000000), long(3000), long(3000), long(3000), long(3000), long(3000), long(3000), long(3000)
    ]
    CHECKSUMS = [
        'md5:5479b5d005f65a792a029c5d4f096261', #0
        'md5:2fbb709bb3fd03440828d190abd489c3',
        'md5:0f85f74981f8cc8b9f45a9469c869940',
        'md5:0f85f74981f8cc8b9f45a9469c869940',
        'md5:0f85f74981f8cc8b9f45a9469c869940', #5
        'md5:0f85f74981f8cc8b9f45a9469c869940',
        'md5:0f85f74981f8cc8b9f45a9469c869940',
        'md5:0f85f74981f8cc8b9f45a9469c869940'
    ]
    OWNERS = ['/C=CH O=CERN P=DQ2 testcase owner/CN=DQ2 testcase owner', '/C=CH O=CERN P=DQ2 testcase owner/CN=Attacker!!!']
    DUIDS = ['d0000000-0000-0000-0000-000000000000', 'd0000000-0000-0000-0000-000000000001', 'd0000000-0000-0000-0000-000000000002', 'd0000000-0000-0000-0000-000000000003']
    VUIDS = ['f0000000-0000-0000-0000-000000000000', 'a0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000003', 'e0000000-0000-0000-0000-000000000004', 'a0000000-0000-0000-0000-000000000005', 'a0000000-0000-0000-0000-000000000006', 'b0000000-0000-0000-0000-000000000007']
    INVERTED_VUIDS = VUIDS + []
    INVERTED_VUIDS.reverse()