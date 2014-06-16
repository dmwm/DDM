#!/bin/sh

function command(){                                  
     echo "----->" $@ >> $logfile 2>&1                                  
     eval $@          >> $logfile 2>&1                               
}               

MAILTO=insert_MAILTO
CRONPATH=`dirname $0`

logfileName=cron_`date +\%Y-\%m-\%d_\%H-\%M-\%S`.log
logfile=$CRONPATH/../log/$logfileName

command "hostname"

export TNS_ADMIN=/etc

command "cd $CRONPATH/.."

startDate="`date -d '-1 day' +\%Y-\%m-\%d` 00:00:00"
endDate="`date +\%Y-\%m-\%d` 00:00:00"

command "python2.6 $CRONPATH/popdbDaemon.py  -w 4 -s \"$startDate\"  -e \"$endDate\" -v -b" 

[ $? -ne 0 ] &&  cat $logfile | mail -s "Problem in PopDB CRAB cronJob of $logfileName" $MAILTO && exit

command "python2.6 $CRONPATH/popdbRefresh.py  -w 4 -s \"$startDate\"  -e \"$endDate\" -v -b -l " 

[ $? -ne 0 ] &&  cat $logfile | mail -s "Problem in PopDB CRAB cronJob of $logfileName" $MAILTO && exit

cat $logfile | mail -s "PopDB cronJob of $logfileName" $MAILTO

echo "-----> removing cache file in $CRONPATH/../cache/" >> $logfile

rm -fv $CRONPATH/../cache/dashb-cms-datapop* >> $logfile

