#!/usr/bin/env python

from __future__ import print_function
import subprocess
import cx_Oracle
import datetime
import re
from optparse import OptionParser
from operator import itemgetter

parser = OptionParser()

parser.add_option('--dbconn', dest='dbconn', help='file containing DB connection string')

(options, args) = parser.parse_args()

f = open(options.dbconn)
connstring=f.read().rstrip()
f.close()

conn = cx_Oracle.connect(connstring)

curs = cx_Oracle.Cursor(conn)

p = subprocess.Popen(["/usr/bin/eos", "ls", "/eos/cms/store/group"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

while True:
    group = p.stdout.readline().rstrip()
    if not group and not p.poll():
        break
    else:
        print("=========================================================================")
        print(group)
        q=subprocess.Popen(["/usr/bin/eos", "quota", "ls", "-m", "-g", "zh", "/eos/cms/store/group/%s" % group ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out2, err2 = q.communicate()
        print(out2)
        print()

        alldirs={}

        q2=subprocess.Popen(["/usr/bin/eos", "find", "-d", "/eos/cms/store/group/%s" % group ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while True:
            path = q2.stdout.readline().rstrip()
            if not path:
                break
            else:
                if path.split()[2]!='nfiles=0':
                    mydir=path.split()[0]
                    q3=subprocess.Popen(["/usr/bin/eos", "fileinfo", mydir, "-m"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    fileinfo = q3.stdout.read()
                    if fileinfo:
                        alldirs[re.sub(re.compile('^/eos/cms'), '', fileinfo.split()[1].split('=')[1])]=datetime.date.fromtimestamp(float(fileinfo.split()[4].split('=')[1]))

        query="SELECT MAX_TDAY as \"LAST ACCESS\", MIN_TDAY as \"FIRST ACCESS\", READ_BYTES as \"MB READ     \", READ_ACC as \"N ACCESSES\", PATH from V_XRD_STAT2_AGGR1 where path like '/store/group/"+group+"/%' or path like '/eos/cms/store/group/"+group+"/%' ORDER BY MAX_TDAY ASC, READ_ACC DESC, READ_BYTES DESC"
        
        curs.execute(query)
        results=curs.fetchall()
        
        header ='LAST_ACCESS\tFIRST_ACCESS\tCHANGE_TIME\tMB_READ\t\tN_ACCESSES\tPATH'

        print(header)

        popdirs={}

        for row in results:
            popdirs[re.sub(re.compile('^/eos/cms'), '', row[4])]=(row[0].date(), row[1].date(), row[2], row[3])

        popandunpopdirs=[]

        for direc in alldirs:
            try:
                populardir=popdirs[direc]
                popandunpopdirs.append((popdirs[direc][0], popdirs[direc][1], alldirs[direc], popdirs[direc][2], popdirs[direc][3], direc,))
            except KeyError:
                popandunpopdirs.append((datetime.date.fromtimestamp(0), datetime.date.fromtimestamp(0), alldirs[direc], 0, 0, direc,))


        sorteddirs = sorted(popandunpopdirs, key=itemgetter(2))
        sorteddirs = sorted(sorteddirs, key=itemgetter(4, 3), reverse=True)
        sorteddirs = sorted(sorteddirs, key=itemgetter(0, 1))
    

        for direc in sorteddirs:
            print(str(direc[0])+"\t"+str(direc[1])+"\t"+str(direc[2])+"\t"+("{0:.2f}".format(direc[3])).rjust(10, ' ')+"\t"+str(direc[4])+"\t"+direc[5])

        print("=========================================================================")
        print()

