"""
Contains the CollectMessages class definition.

NEED TO LOOK AT: log information, what to write to the log file

@license: Apache License 2.0
"""
"""
Copyright (c) Members of the EGEE Collaboration. 2004.
See http://www.eu-egee.org/partners/ for details on the copyright holders.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.

You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
"""

import time
import simplejson as json
import socket
import sys

from dashboard.common.ExistsException import ExistsException
from dashboard.common import log as logging
from dashboard.service.config.Service import Service

import SocketServer
import string

from messaging.message import Message
from messaging.queue.dqs import DQS

import threading

global gmq
global glogger
global gcounter
gcounter =0

class CMSSWUDPHandler(SocketServer.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def __del__(self):
        if gcounter % 100 == 0:
            glogger.info('Current Thread %s  - Num msg uploaded %s' % (threading.current_thread().name,gcounter))

    def handle(self):
        try:
            data = self.request[0].strip()
            socket = self.request[1]
            #glogger.info("%s wrote:" % (self.client_address[0]))
            jsonDict = data.replace('\n',' ')

            msg = Message(body=jsonDict)
        
            try:
                mqid = gmq.add_message(msg)
                #glogger.info("msg added as %s" % mqid)
            except Exception,  err :
                glogger.error( "failing upload to local queue. Error: %s" % (err))
                raise Exception
            global gcounter
            gcounter += 1
        except Exception,  err :
            glogger.error( "Error: %s" % (err))
            
class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer): pass
        
class CMSSWUDPListener(Service):
    """                                                                                                                                                                                            
    Class definition of the dashboard CMSSWUDPListener agent.                                                                                                                                     
    """
    _logger = logging.getLogger("dashboard.popdb-cmssw.CMSSWUDPListener")
    global glogger
    glogger = _logger

    def __init__(self, name, configFile):
        """
        Initializer for the object.
        """
        Service.__init__(self, name, configFile)
        
        self.id = self.param('id')
        self.udp_port = int(self.param('udp_port'))
        self.udp_host = self.param('udp_host')
        if self.udp_host == 'hostname':
            self.udp_host = socket.gethostname()

        try:
            global gmq
            gmq = DQS(path = self.param('localQueue'))
            self._logger.info( "Created connection to local queue %s" % self.param('localQueue'))
        except Exception,  err :
            self._logger.error( "Failing connection to local queue %s" % (err))
            raise Exception

        self._logger.info('UDP listener on %s:%s'%(self.udp_host,self.udp_port))
        self.server = ThreadedUDPServer((self.udp_host,self.udp_port),CMSSWUDPHandler)   

        self._logger.info('created server. going to serve_forever in thread')
        self.server_thread = threading.Thread(target=self.server.serve_forever)

        self.server_thread.start()
        self._logger.info('Server loop running in thread: %s' % self.server_thread.name )


    def run(self):
        """
        Main function of the service. While it is running it serves forever the UDPServer 
        from the messaging server into the database.
        """
        try:
            counter = 0
            self._logger.info('...now run forever')
            while self.status() is not None:
                pass
                        
        except Exception,  err :
            self._logger.error( "%s" % (err))
            self.server.shutdown()
            raise Exception
        
        
            

    

