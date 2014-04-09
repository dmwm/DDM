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
from dashboard.dao.DAOFactory import DAOFactory
from dashboard.dao.DAOContext import DAOContext
from dashboard.service.config.Service import Service
from datetime import datetime

from messaging.message import Message
from messaging.queue.dqs import DQS

class CMSSWMonCollector(Service):
    """                                                                                                                                                                                            
    Class definition of the dashboard CMSSWMonCollector agent.                                                                                                                                     
    """
    _logger = logging.getLogger("dashboard.collector.CMSSWMonCollector")

    def __init__(self, name, configFile):
        """
        Initializer for the object.
        """
        Service.__init__(self, name, configFile)

        # Hourly purge
        self.PURGE_INTERVAL = 3600

        # DB Table where to store the messages
        self.transfers_db_table = self.param('transfersDBTable')
        self.transfers_db_table_rejected = self.param('rejectedDBTable')
        # Maximum number of messages in the buffer when making a bulk insert 
        self.buffer_size = int(self.param('bufferSize'))

        self.id = self.param('id')
        self.dbsection = self.param('dbsection')  

        self._next_purge = time.time() + self.PURGE_INTERVAL

        # Try to read the local queue
        try:
            self.localQueue = DQS(path = self.param('localQueue'))
        except Exception, e:
            self._logger.error("connection to the local queue failed")

    def run(self):
        """
        Main function of the service. While it is running it inserts messages 
        from the messaging server into the database.
        """
        while self.status() is not None:
            (names, bodies) = ([], [])
            msgCount = 0
            #try:
            for name in self.localQueue:
                if self.localQueue.lock(name):
                    msg = self.localQueue.get_message(name)
                    self.decode_message(msg, bodies)
                    names.append(name)
                    msgCount += 1

                    # Exit the loop when X messages collected
                    if (msgCount >= self.buffer_size):
                        break

            (successes, failures, ellapsed_time, bulk) = self.insert_messages(names, bodies)
            self._logger.info(
                "%d messages to insert for %s, %d successfully and %d failed in %d ms (bulk = %s)"
                % (msgCount, self.id, successes, failures, ellapsed_time, str(bulk))
            )

            self.purge() 

            # Prevent the buffer to run continuously when buffer is not full
            if msgCount != self.buffer_size:
                time.sleep(5)
    
    
    def JSON_format(self, message):
        """
        Decodes messages in JSON format to a dictionary python
        """
        if message.find(chr(4)): # If the last character is an ascii End of Transmission character we need to remove it
            return json.loads(message.split(chr(4))[0])
        else: return json.loads(message)
    
    
    def delete_messages(self, names):
        """
        """
        for name in names:
            self.localQueue.remove(name)

    def purge(self):
        if time.time() < self._next_purge:
            return
        self.localQueue.purge(60, 60)  
        self._next_purge = time.time() + self.PURGE_INTERVAL
    
    def insert_messages(self, names, bodies):
        """
        """
        start = time.time()
        successes, failures, ellapsed_time, is_bulk = 0, 0, 0, True

        (ctx, dao) = (None, None)
        try:
            # Get a site DAO to work with
            ctx = DAOContext.getDAOContext(section=self.dbsection) 
            dao = DAOFactory.getDAOFactory().getDAOObject(ctx,'xrootd','XRootDDAO')
            
            # Try to make a bulk insert 
            if len(bodies) > 0:
                try:
                    dao.insertMessages(bodies, self.transfers_db_table)
                    successes = len(bodies)
                except Exception, msg:
                    is_bulk = False
                    self._logger.warning("couldn't feed all the data: %s" % msg)
                    self._logger.warning("inserting messages one by one")

                    # Try to insert the messages one by one if any exception
                    for body in bodies: 
                        try:
                            dao.insertMessages(body, self.transfers_db_table)
                            successes += 1
                        except Exception, msg:
                            failures += 1

                            # Try to insert the malformed message in a table without any constraint
                            if self.transfers_db_table_rejected is not None:
                                try:
                                    body['exception'] = str(msg)
                                    dao.insertMessages(body, self.transfers_db_table_rejected)
                                except:
                                    self._logger.warning("Couldn't feed data: %s" % msg)

            ctx.commit()
            self.delete_messages(names)

        except Exception, msg:
            # maybe it would be necessary to manage if something is wrong in the database (downtime for instance)
            self._logger.error("%s" % msg)
            ctx.destroy()
            raise Exception
        end = time.time()
        ms = 1000 * (end - start)
        return (successes, failures, int(ms), is_bulk)

    def decode_message(self, message, bodies):
        """
        """
        try:
            body = message.get_body()
            body = body.replace(', ,',',')
            msgDict = self.JSON_format(body)
            try:
                if msgDict['fallback'] == True:
                    msgDict['fallback'] = '1'
                else:
                    msgDict['fallback'] = '0'
            except:
                msgDict['fallback'] = '-'

            #self._logger.info(msgDict)
        
            bodies.append(msgDict)

        except ValueError, msg:
            self._logger.warning("Impossible to decode the message: %s by JSON" % message)
            self._logger.error(msg)
            #raise msg
        except Exception, msg:
            self._logger.warning("Exception: %s" % msg)

