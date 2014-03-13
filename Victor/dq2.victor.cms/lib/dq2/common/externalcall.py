"""
Module for handling external process calls. 

@author: Miguel Branco
@contact: miguel.branco@cern.ch
@since: 1.0
@version: $Id: externalcall.py,v 1.1 2008-05-19 13:16:09 mbranco Exp $
"""
import os
import signal
import sys
import time
import tempfile

class ExternalCallException(Exception):
    pass

class ExternalCallTimeOutException(ExternalCallException):
    pass

def call(cmd, min_secs=1, timeout_secs=30, interval_secs=1, kill_on_timeout=True):
    """
    Do external call by spawning new process.
    
    @raise ExternalCallException: In case of error.
    @raise ExternalCallTimeOutException: In case of timeout.
    
    @return: Tuple with status, output
    """
    cmd = cmd.strip()
    try:
        output = tempfile.mktemp()
    except RuntimeWarning:
        pass
    except:
        raise ExternalCallException("Could not create temporary file.")
    startTime = time.time()
    try:
        childPid = os.fork()
    except:
        raise ExternalCallException("Could not spawn process to serve '%s'." % cmd)
    if childPid == 0:
        try:
            # child process
            os.setpgrp() # group leader
            # redirect outputs to file
            f = open(output, 'w')
            os.dup2(f.fileno(), sys.stdout.fileno())
            os.dup2(f.fileno(), sys.stderr.fileno())
            # execute ...
            args = cmd.split(' ')
            os.execvp(args[0], args)
        finally:
            os._exit(1)
    # parent process
    time.sleep(min_secs)
    exitCode = None
    finished = False
    while time.time() - startTime < timeout_secs:
        try:
            pid, exitCode = os.waitpid(childPid, os.P_NOWAIT)
            if pid == 0: # not finished
                time.sleep(interval_secs)
                continue
            elif pid > 0: # done
                finished = True
                break
        except:
            break
    try:
        if finished: # read output file
            f = open(output, 'r')
            ll = f.readlines()
            f.close()
            return exitCode, ''.join(ll) 
        # timed out
        if kill_on_timeout:
            os.killpg(childPid, signal.SIGKILL)
        time.sleep(1)
        # wait for any child process without hanging
        try:
            r = os.waitpid(-1, os.WNOHANG)
        except:
            pass
        raise ExternalCallTimeOutException("Call to '%s' timed out." % cmd)
    finally:
        try: # always remove temporary file
            os.remove(output)
        except:
            pass
