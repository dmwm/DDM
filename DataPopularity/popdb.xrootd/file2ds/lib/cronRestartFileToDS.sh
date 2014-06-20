#!/bin/sh

function command(){
     echo "----->" $@ >> $logfile 2>&1
     eval $@          >> $logfile 2>&1
     return $?
}

MAILTO=insert_MAILTO
CRONPATH=`dirname $0`

logfileName=cron_`date +\%Y-\%m-\%d_\%H-\%M-\%S`.log
logdir=$CRONPATH/../log/
logfile=$logdir/$logfileName

n=`ps -ef | grep "$CRONPATH/fileToDataSetAssociationTest.py" | grep -c python `
[ "$n" != "0" ] && exit

command "hostname"
command "echo $USER"

export TNS_ADMIN=/etc
command 'echo $TNS_ADMIN'

[ ! -d $logdir ] && mkdir $logdir

command "cd $CRONPATH/.."
command "python2.6 $CRONPATH/fileToDataSetAssociationTest.py -v &"
exitStatus=$?

[ $exitStatus -ne 0 ] &&  cat $logfile | mail -s "Problem in fileToDataSetAssociation of $logfileName" $MAILTO


