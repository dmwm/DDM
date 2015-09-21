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

startHour=0
window=4

while [ $startHour -lt 24 ]; do

    endHour=$((startHour+window))
    
    startHourStr=0$startHour
    startHourStr=${startHourStr: -2}

    endHourStr=0$endHour
    endHourStr=${endHourStr: -2}

    startDate="`date -d '-1 day' +\%Y-\%m-\%d` "$startHourStr":00:00"

    if [ $endHour -lt 24 ]; then
	endDate="`date -d '-1 day' +\%Y-\%m-\%d` "$endHourStr":00:00"
    else
	endDate="`date +\%Y-\%m-\%d` 00:00:00"
    fi

    command "python2.6 $CRONPATH/popdbDaemon.py  -w 4 -s \"$startDate\"  -e \"$endDate\" -v -b" 
    
    [ $? -ne 0 ] &&  cat $logfile | mail -s "Problem in PopDB CRAB cronJob of $logfileName" $MAILTO && exit
    
    startHour=$endHour
done

command "python2.6 $CRONPATH/popdbRefresh.py  -w 4 -s \"$startDate\"  -e \"$endDate\" -v -b -l " 

[ $? -ne 0 ] &&  cat $logfile | mail -s "Problem in PopDB CRAB cronJob of $logfileName" $MAILTO && exit

cat $logfile | mail -s "PopDB cronJob of $logfileName" $MAILTO

echo "-----> removing cache file in $CRONPATH/../cache/" >> $logfile

rm -fv $CRONPATH/../cache/dashb-cms-datapop* >> $logfile

