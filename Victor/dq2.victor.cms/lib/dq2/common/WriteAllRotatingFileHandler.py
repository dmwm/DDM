from logging import handlers
import os, stat

class WriteAllRotatingFileHandler(handlers.RotatingFileHandler):
    
    def __init__(self, filename, mode='a', maxBytes=0, backupCount=0, encoding=None):         
        handlers.RotatingFileHandler.__init__ (self, filename, mode, maxBytes, backupCount, encoding)
        currMode = os.stat(self.baseFilename).st_mode
        os.chmod(self.baseFilename, 16895 )
         
    
    def doRollover(self):
        """
        Override base class method to make the new log file group writable.
        """
        handlers.RotatingFileHandler.doRollover(self)
        currMode = os.stat(self.baseFilename).st_mode
        os.chmod(self.baseFilename, 16895)
