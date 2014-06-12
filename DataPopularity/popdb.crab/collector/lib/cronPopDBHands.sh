#!/bin/sh

function command(){                                  
     echo "----->" $@ >> $logfile 2>&1                                  
     eval $@          >> $logfile 2>&1                               
}               
  
[ $# -ne 2 ] && echo 'Usage: ./cronPopDBHands.sh <startDate> <endDate> (date format: "YYYY-MM-DD HH24:MI:SS")' && exit 1

startDate=$1
endDate=$2

CRONPATH=`dirname $0`

logfile=$CRONPATH/../log/cron_`date +\%Y-\%m-\%d_\%H-\%M-\%S`.log

hostname > $logfile

export TNS_ADMIN=/etc

command "cd $CRONPATH/.."

command "python2.6 $CRONPATH/popdbDaemon.py  -w 4 -s \"$startDate\"  -e \"$endDate\" -v -b " 


