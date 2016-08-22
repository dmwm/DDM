#!/bin/sh

function changeOwner(){
    [ ! -d $1  ] &&  mkdir -p $1 
    chown -R $POPDBUSER $1 
    echo 'chown for ' $1
}
# This is the user that will own the binaries
POPDBUSER=${POPDBUSER:=cmspopdb}
POPDB_NOTIFICATION=${POPDB_NOTIFICATION:=cms-popdb-alarms@cern.ch}

echo "User that will run the service is $POPDBUSER"
echo "EMAIL notification address is ${POPDB_NOTIFICATION}"

sed -i "s@cmspopdb@$POPDBUSER@" /etc/cron.d/xrootd_popularity_file2ds
sed -i "s;insert_MAILTO;${POPDB_NOTIFICATION};" /etc/cron.d/xrootd_popularity_file2ds
sed -i "s;insert_MAILTO;${POPDB_NOTIFICATION};" /opt/CMSDataPopularity/xrootd/lib/cronRestartFileToDS.sh
sed -i "s;insert_MAILTO;${POPDB_NOTIFICATION};" /etc/cron.d/xrootd_popularity_checkmviews

changeOwner /opt/CMSDataPopularity/xrootd
changeOwner /opt/CMSDataPopularity/xrootd/log
changeOwner /opt/CMSDataPopularity/xrootd/.


