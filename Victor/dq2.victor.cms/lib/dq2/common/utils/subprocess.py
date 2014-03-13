"""

@author:
@contact:
@since: 0.3.0
@version: $Id: subprocess.py,v 1.1 2008-05-29 11:15:40 psalgado Exp $

@deprecated: this module will be removed in the next version of dq2-common.

@see: http://ganga.web.cern.ch/ganga/release/4.3.2/reports/latest/html/coverage/summary/GangaLHCb/SubprocessExecuter.py.html
"""

import time
import select
import os
import re
import sys
import popen2


ERROR = 'Error'


def S_ERROR (sMessage=''):
    return { 'Status': ERROR, 'OK' : 0, 'Message' : sMessage  }


def S_OK (sValue=None, sPname='Value'):
    dResult = { 'Status': 'OK', 'OK' : 1 }
    if sValue is not None:
        dResult[ sPname ] = sValue
    return dResult


class SubprocessExecuter:


    def __init__ (self, iTimeout = False):
        """
        """
        self.changeTimeout(iTimeout)
        self.iBufferLimit = 5242880 # 5MB limit for data


    def changeTimeout (self, iTimeout):
        """
        """
        self.iTimeout = iTimeout
        if self.iTimeout == 0:
            self.iTimeout = False
        
    def __readFromPipe (self, oPipe, iBaseLength=0):
        """
        """
        sData = ""
        iMaxSliceLength = 8192
        iLastSliceLength = 8192
        
        while iLastSliceLength == iMaxSliceLength:
            sReadBuffer = os.read( oPipe, iMaxSliceLength )
            iLastSliceLength = len( sReadBuffer )
            sData += sReadBuffer
            if len( sData ) + iBaseLength > self.iBufferLimit:
                dRetVal = S_ERROR( "Reached maximum allowed length (%d bytes) for called function return value" % self.iBufferLimit )
                dRetVal[ 'ReadData' ] = sData
                return dRetVal
            
        return S_OK( sData )


    def __executePythonFunction (self, oFunc, stArgs, oWritePipe):
        """
        """
        try:
            os.write( oWritePipe, "%s\n" % str( S_OK( oFunc( *stArgs ) ) ) )
        except Exception, v:        
            try:
                os.write( oWritePipe, "%s\n" % str( S_ERROR( str( v ) ) ) )
            except :
                pass                    
        try:
            os.close( oWritePipe )
        finally:
            os._exit(0)


    def __selectFD (self, lR, iTimeout=False):
        """
        """
        if self.iTimeout and not iTimeout:
            iTimeout = self.iTimeout
        if not iTimeout: 
            return select.select( lR , [], [] )[0]
        else:
            return select.select( lR , [], [], iTimeout )[0]


    def pythonCall (self, oFunction, stArgs):
        """
        """
        oReadPipe, oWritePipe = os.pipe()
        iPid = os.fork()
        if iPid == 0:
            os.close( oReadPipe )
            self.__executePythonFunction( oFunction, stArgs, oWritePipe )
            os.close( oWritePipe )
        else:
            os.close( oWritePipe )
            lReadable = self.__selectFD( [ oReadPipe ] )
            if len( lReadable ) == 0:
                os.close( oReadPipe )
                os.kill( iPid, 9 )
                os.waitpid( iPid, 0 )
                return S_ERROR( "%d seconds timeout for '%s' call" % ( self.iTimeout, oFunction.__name__ ) )
            elif lReadable[0] == oReadPipe:
                dData = self.__readFromPipe( oReadPipe )
                os.close( oReadPipe )
                os.waitpid( iPid, 0 )
                if dData[ 'OK' ]:
                    return eval( dData[ 'Value' ] )
                return dData


    def __generateSystemCommandError (self, sMessage):
        """
        """
        retVal = S_ERROR(sMessage)
        retVal[ 'stdout' ] = self.lBuffers[0][0]
        retVal[ 'stderr' ] = self.lBuffers[1][0]
        return retVal


    def __readFromFile (self, oFile, iBaseLength, bAll):
        """
        """
        try:
            if bAll:
                sData = "".join( oFile.readlines() )
            else:
                sData = oFile.readline()
        except Exception, v:
            pass 
        if sData == "":
            #self.checkAlive()
            self.bAlive = False
        if len( sData ) + iBaseLength > self.iBufferLimit:
            dRetVal = S_ERROR( "Reached maximum allowed length (%d bytes) for called function return value" % self.iBufferLimit )
            dRetVal[ 'ReadData' ] = sData
            return dRetVal
            
        return S_OK( sData )


    def __readFromSystemCommandOutput (self, oFile, iDataIndex, bAll=False):
        """
        """
        retVal = self.__readFromFile( oFile, len( self.lBuffers[ iDataIndex ][0] ), bAll )
        if retVal[ 'OK' ]:
            self.lBuffers[ iDataIndex ][0] += retVal[ 'Value' ]
            if not self.oCallback == None:
                while self.__callLineCallback( iDataIndex ):
                    pass
            return S_OK()
        else:
            self.lBuffers[ iDataIndex ][0] += retVal[ 'ReadData' ]
            os.kill( self.oChild.pid, 9 )
            self.oChild.wait()
            return self.__generateSystemCommandError("Exceeded maximum buffer size ( %d bytes ) timeout for '%s' call" % (self.iBufferLimit, self.sCmd ))


    def systemCall (self, sCmd, oCallbackFunction = None):
        """
        """
        self.sCmd = sCmd
        self.oCallback = oCallbackFunction
        self.oChild = popen2.Popen3( self.sCmd, True )
        self.lBuffers = [ [ "", 0 ], [ "", 0 ] ]
        iInitialTime = time.time()
        iExitStatus = self.oChild.poll()
        
        while iExitStatus == -1:
            retVal = self.__readFromCommand()
            if not retVal[ 'OK' ]:
                return retVal
            if self.iTimeout and time.time() - iInitialTime > self.iTimeout:
                os.kill( self.oChild.pid, 9 )
                self.oChild.wait()
                self.__readFromCommand( True )
                self.oChild.fromchild.close()
                self.oChild.childerr.close()
                return self.__generateSystemCommandError( "Timeout (%d seconds) for '%s' call" % ( self.iTimeout, sCmd ) )
            iExitStatus = self.oChild.poll()
        
        self.__readFromCommand(True )
        
        self.oChild.fromchild.close()
        self.oChild.childerr.close() 
        if iExitStatus > 256:
          iExitStatus /= 256
        return S_OK( ( iExitStatus, self.lBuffers[0][0], self.lBuffers[1][0] ) )


    def __readFromCommand (self, bLast=False):
        """
        """
        if bLast:
            retVal = self.__readFromSystemCommandOutput( self.oChild.fromchild, 0, True )
            if not retVal[ 'OK' ]:
                return retVal
            retVal = self.__readFromSystemCommandOutput( self.oChild.childerr, 1, True )
            if not retVal[ 'OK' ]:
                return retVal
        else:
            lReadable = self.__selectFD( [ self.oChild.fromchild, self.oChild.childerr ], 1 )
            if self.oChild.fromchild in lReadable:
                retVal = self.__readFromSystemCommandOutput( self.oChild.fromchild, 0 )
                if not retVal[ 'OK' ]:
                    return retVal
            if self.oChild.childerr in lReadable:
                retVal = self.__readFromSystemCommandOutput( self.oChild.childerr, 1 )
                if not retVal[ 'OK' ]:
                    return retVal
        return S_OK()


    def __callLineCallback (self, iIndex):
        """
        """
        iNextLine = self.lBuffers[ iIndex ][0][ self.lBuffers[ iIndex ][1]: ].find( "\n" )
        if iNextLine > -1:
            self.oCallback( iIndex, self.lBuffers[ iIndex ][0][ self.lBuffers[ iIndex ][1]: self.lBuffers[ iIndex ][1] + iNextLine ] )
            self.lBuffers[ iIndex ][1] += iNextLine + 1 
            return True
        return False


def exeCommand (sCmd, iTimeout = 0, oLineCallback=None):
    """
    Return ( status, output, error, pythonError ) of executing cmd in a shell.
    
    @rtype: tuple
    """
    
    oSPE = SubprocessExecuter( iTimeout )
    retVal = oSPE.systemCall( sCmd, oLineCallback )
    if retVal[ 'OK' ]:
        return retVal[ 'Value' ][0], retVal[ 'Value' ][1], retVal[ 'Value' ][2], 0
    else:
        if re.search("Timeout",retVal['Message']):
          return 1, retVal['stdout'], retVal['Message'], 2
        else:  
          return 1, retVal['stdout'], retVal['stderr'], 1


def exeFunction (sCmd, Args, iTimeout = 0):
    """
    Return ( status, output, error, pythonError ) of executing function.
    
    @rtype: tuple
    """
    oSPE = SubprocessExecuter( iTimeout )
    retVal = oSPE.pythonCall( sCmd, Args)
    return retVal


def exeCommandWithFilter (cmd, filterHandle=None):
    """
    Executes command cmd with output filter 
    
    Executes command cmd with each line in stdout passed to the filterFunction
    """
    if not filterHandle:
        return exeCommand(cmd)
    
    print cmd
    proc = Popen3(cmd,True,10000)
    sts = -1
    out = ''
    error = ''
    
    while 1:
        
        print 'Trying to readline'
        outline = os.read(proc.fromchild.fileno(),10)
        print "Got",outline
        out = out+outline
        
        filterHandle(outline)
        time.sleep(1)
        sts = proc.poll()
        print "sts:",sts
        if sts != -1:
            output = proc.fromchild.read()
            out = out + output
            lines = output.split('\n')
            for line in lines:
                filterHandle(line)
            break
        time.sleep(1)
    
    error = proc.childerr.read()
    if sts is None: sts = 0
    # Extract the pure status code
    if sts > 255 : sts = sts/256
    if out[-1:] == '\n': out = out[:-1]
    if error[-1:] == '\n': error = error[:-1] 
    return sts, out, error
