#!/usr/bin/env python

import shutil
import fileinput
import sys
from subprocess import call
from optparse import OptionParser

parser = OptionParser()
parser.add_option('-d','--dev', action="store_true", dest='develop', default=False, help='Set development mode. No grants will be set for reader and writer accounts.')
parser.add_option('-p','--prod', action="store_true", dest='production', default=False, help='Set production mode. Grants for the reader and writer accounts will be set.')
parser.add_option('-s','--set-accounts', action="store_true", dest='accounts', default=False, help='Use accounts differing from the default CMS_CLEANING_AGENT.')
parser.add_option('--database', type='string', dest='database', default='cmsr', help='Database to which the schema will be applied.')
parser.add_option('--reader-account', type='string', dest='reader_acct', default='CMS_CLEANING_AGENT_R', help='Database account, which will be used as reader.')
parser.add_option('--writer-account', type='string', dest='writer_acct', default='CMS_CLEANING_AGENT_W', help='Database account, which will be used as writer.')
parser.add_option('--admin-account', type='string', dest='admin_acct', default='CMS_CLEANING_AGENT', help='Database account, which will be used as admin.')
parser.add_option('--admin-password', type='string', dest='admin_passwd', default='', help='Password of the admin account for the database.')
parser.add_option('--reader-password', type='string', dest='reader_passwd', default='', help='Password of the reader account for the database.')
parser.add_option('--writer-password', type='string', dest='writer_passwd', default='', help='Password of the writer account for the database.')
(options,args)=parser.parse_args()

if options.develop and options.production:
    print "production and development mode specified.\n Asuming production mode."
db_schemas = ['victor_schema.sql']
if options.production:
    db_schemas.append('grants.sql')
if options.reader_acct or options.writer_acct:
    db_schemas.append('synonyms.sql')

if options.accounts:
    for schema in db_schemas:
        shutil.copyfile(schema,'tmp_'+schema)
        for line in fileinput.input('tmp_'+schema,inplace=1):
            if 'CMS_CLEANING_AGENT_R' in line:
                line = line.replace('CMS_CLEANING_AGENT_R',options.reader_acct)
            if 'CMS_CLEANING_AGENT_W' in line:
                line = line.replace('CMS_CLEANING_AGENT_W',options.writer_acct)
            if 'CMS_CLEANING_AGENT' in line:
                line = line.replace('CMS_CLEANING_AGENT',options.admin_acct)
            sys.stdout.write(line)

if options.admin_acct and options.admin_passwd:
    for schema in db_schemas:
        if schema == 'synonyms.sql':
            for acct,passwd in [(options.reader_acct,options.reader_passwd),(options.writer_acct,options.writer_passwd)]:
                if acct and passwd:
                    call('sqlplus -S '+acct+'/'+passwd+'@'+options.database+' < tmp_'+schema, shell=True)
            call(['rm','tmp_'+schema])
        else:
            call('sqlplus -S '+options.admin_acct+'/'+options.admin_passwd+'@'+options.database+' < tmp_'+schema, shell=True)
            call(['rm','tmp_'+schema])
