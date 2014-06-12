#!/bin/sh

function command(){                                  
     echo "----->" $@ >> $logfile 2>&1                                  
     eval $@          >> $logfile 2>&1                               
}               

MAILTO=insert_MAILTO
CRONPATH=`dirname $0`

logfile=$CRONPATH/../log/cron_`date +\%Y-\%m-\%d_\%H-\%M-\%S`.log

command "hostname"

export TNS_ADMIN=/etc

command "cd $CRONPATH/.."

startDate="`date -d '-1 day' +\%Y-\%m-\%d` 00:00:00"
endDate="`date +\%Y-\%m-\%d` 00:00:00"

command "python2.6 $CRONPATH/popdbRefresh.py  -w 4 -s \"$startDate\"  -e \"$endDate\" -v -b -l " 

[ $? -ne 0 ] &&  cat $logfile | mail -s "Problem in PopDBREFRESH cronJob" $MAILTO && exit

cat $logfile | mail -s "PopDBREFRESH cronJob" $MAILTO


