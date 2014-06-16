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

#useradd --shell /bin/bash --create-home --home-dir /home/cern cern
/usr/sbin/useraddcern cmspopdb

sed -i "s@cmspopdb@$POPDBUSER@" /etc/cron.d/crab_popularity_collector
sed -i "s;insert_MAILTO;${POPDB_NOTIFICATION};" /etc/cron.d/crab_popularity_collector
sed -i "s;insert_MAILTO;${POPDB_NOTIFICATION};" /opt/CMSDataPopularity/crab/lib/cronPopDB.sh
sed -i "s;insert_MAILTO;${POPDB_NOTIFICATION};" /opt/CMSDataPopularity/crab/lib/cronPopDBRefresh.sh

changeOwner /opt/CMSDataPopularity/crab
changeOwner /opt/CMSDataPopularity/crab/log
changeOwner /opt/CMSDataPopularity/crab/cache
changeOwner /opt/CMSDataPopularity/crab/.


