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

startTime=$(date -d "$startDate" -u +%s)
endTime=$(date -d "$endDate" -u +%s)

window=2

endWindowTime=$startTime

while [ $endWindowTime -lt $endTime ]; do

    endWindowTime=$((startTime+(window*3600)))

    startWindowDate="`date -u -d @$startTime +\%Y-\%m-\%d\ \%H:\%M\:%S`"

    if [ $endWindowTime -lt $endTime ]; then
	endWindowDate="`date -u -d @$endWindowTime +\%Y-\%m-\%d\ \%H:\%M\:%S`"
    else
	endWindowDate=$endDate
    fi

    command "python2.6 $CRONPATH/popdbDaemon.py  -w $window -s \"$startWindowDate\"  -e \"$endWindowDate\" -v -b"

    [ $? -ne 0 ] &&  cat $logfile | mail -s "Problem in PopDB CRAB cronJob of $logfileName" $MAILTO && exit

    startTime=$endWindowTime

done



