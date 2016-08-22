#! /usr/bin/env python26

from __future__ import print_function

import json
import cx_Oracle

config = open('./etc/auth.txt')
auth_params = json.loads(config.read())
connection_string = auth_params['DB_CONN_STRING']
connection = cx_Oracle.Connection(connection_string)
cursor = cx_Oracle.Cursor(connection)
query = '''select mview_name, last_refresh_date from user_mviews
             where sysdate-last_refresh_date>1 order by last_refresh_date'''
results = cursor.execute(query).fetchall()
for row in results:
	print('WARNING: MView %s not refreshed since %s' % (row[0], row[1]))
cursor.close()
connection.close()
