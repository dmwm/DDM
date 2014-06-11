"""
_PopularityException_

General Exception class for Popularity modules

"""

import exceptions
import inspect
import logging
import traceback

class PopularityException(exceptions.Exception):
    """
    _POPException_

    Exception class which works out details of where
    it was raised.

    """
    def __init__(self, message, errorNo = None, **data):
        self.name = str(self.__class__.__name__)
        exceptions.Exception.__init__(self, self.name,
                                      message)

        #  //
        # // Init data dictionary with defaults
        #// 
        self.data = {}
        self.data.setdefault("ClassName", None)
        self.data.setdefault("ModuleName", None)
        self.data.setdefault("MethodName", None)
        self.data.setdefault("ClassInstance", None)
        self.data.setdefault("FileName", None)
        self.data.setdefault("LineNumber", None)
        if errorNo == None:
            self.data.setdefault("ErrorNr", 0)
        else:
            self.data.setdefault("ErrorNr", errorNo)
        
        self._message = message
        self.data.update(data)

        #  //
        # // Automatically determine the module name
        #//  if not set
        if self['ModuleName'] == None:
            frame = inspect.currentframe()
            lastframe = inspect.getouterframes(frame)[1][0]
            excepModule = inspect.getmodule(lastframe)
            if excepModule != None:
                modName = excepModule.__name__
                self['ModuleName'] = modName

                
        #  //
        # // Find out where the exception came from
        #//
        stack = inspect.stack(1)[1]
        self['FileName'] = stack[1]
        self['LineNumber'] = stack[2]
        self['MethodName'] = stack[3]

        #  //
        # // ClassName if ClassInstance is passed
        #//
        if self['ClassInstance'] != None:
            self['ClassName'] = \
              self['ClassInstance'].__class__.__name__


        # Determine the traceback at time of __init__
        self.traceback = str(traceback.format_exc())


    def __getitem__(self, key):
        """
        make exception look like a dictionary
        """
        return self.data[key]

    def __setitem__(self, key, value):
        """
        make exception look like a dictionary
        """
        self.data[key] = value
        
    def addInfo(self, **data):
        """
        _addInfo_

        Add key=value information pairs to an
        exception instance
        """
        for key, value in data.items():
            self[key] = value
        return
        
        
    def __str__(self):
        """create a string rep of this exception"""
        strg = "%s\n" % self.name
        strg += "Message: %s\n" % self._message
        for key, value in self.data.items():
            strg += "\t%s : %s\n" % (key, value, )
        strg += "\nTraceback: \n"
        strg += self.traceback
        strg += '\n'
        return strg

    def getmessage(self):
        return self._message

class Paramvalidationexception(PopularityException):
    def __init__(self, param, cause):
        self.param = param
        self.cause = cause
        PopularityException.__init__(self, 'Error occurred during %s validation, cause: %s' % (self.param, self.cause))

    #def __str__(self):
    #    return 'Error occurred during %s validation, cause: %s' % (self.param, self.cause)


class PopularityDBException(PopularityException):
    def __init__(self, sql, ex):
        self.sql = sql
        self.err = "%s" % ex
        PopularityException.__init__(self, 'Database error occurred: %s (SQL: %s)' % (ex.message, self.sql))

class PopularityConfigException(PopularityException):
    def __init__(self, error):
        self.err = "%s" % error
        PopularityException.__init__(self, 'Configuration file error: %s' % error)
