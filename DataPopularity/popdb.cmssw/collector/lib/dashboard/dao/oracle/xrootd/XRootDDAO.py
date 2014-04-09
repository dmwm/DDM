"""
Contains the definition of a XRootDDAO object
This code actually doesn't run. It is here to illustrate how the Oracle DAO would
look like.

@license: Apache License 2.0
"""
"""
Copyright (c) Members of the EGEE Collaboration. 2004.
See http://www.eu-egee.org/partners/ for details on the copyright holders.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.

You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
"""

import cx_Oracle
import datetime

from cx_Oracle import DatabaseError
from cx_Oracle import IntegrityError

from dashboard.common import log as logging
from dashboard.common.ExistsException import ExistsException
from dashboard.common.InternalException import InternalException


class XRootDDAO(object):
    """
    Abstract class definition of a XRootDDAO object.
    """

    """
    Holds the DAOContext object to be used by this DAO.
    """
    _ctx = None
    _logger = logging.getLogger('dashboard.dao.oracle.transfers.XRootDDAO')

    def __init__(self, ctx):
        """
        Constructor for the XRootDDAO object.
        """
        self._ctx = ctx


    def insertMessages(self, message, database_table):
        """
        Method for inserting messages into databaseTable.
        message can either be a dictionary with key:value where key corresponds
        to the fields in the database or it can be a list of such dictionaries.
        """
        cursor = self._ctx.getCursor()
        sql = "INSERT INTO %s " % database_table
        try:
            if type(message) == dict:
                sql += "( %s ) " % ','.join(message.keys())
                sql += "VALUES (:" + ',:'.join(message.keys()) + ")"
                cursor.execute(sql, message)
            else:
                sql += "( %s ) " % ','.join(message[0].keys())
                sql += "VALUES (:" + ',:'.join(message[0].keys()) + ")"
                cursor.executemany(sql, message)
        except IntegrityError, exc:
            code = exc.args[0].code
            if code == 1:
                self._logger.warn("Message exists :: %s :: %s" % (message, exc))
                raise ExistsException("The message already exists :: %s" % (exc))
            else:
                self._logger.error("Unexpected oracle error :: %s :: %s" % (message, exc))
                raise InternalException("Internal Server Error :: %s" % (exc))
        except DatabaseError, exc:
            self._logger.error("Failed to insert the message :: %s :: %s" % (message, exc))
            raise InternalException("Internal Server Error :: %s" % (exc))
