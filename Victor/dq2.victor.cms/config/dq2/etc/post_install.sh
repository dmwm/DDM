#!/bin/bash

function changeOwner(){
    [ ! -d $1  ] &&  mkdir -p $1 
    chown -R $DASHBUSER $1 
    echo 'chown for ' $1
}
# This is the user that will own the binaries
DASHBUSER=${DASHBUSER:=cmspopdb}
DASHB_NOTIFICATION=${DASHB_NOTIFICATION:=cms-popdb-alarms@cern.ch}

echo "User that will run the service is $DASHBUSER"
echo "EMAIL notification address is ${DASHB_NOTIFICATION}"

#useradd --shell /bin/bash --create-home --home-dir /home/cern cern
#/usr/sbin/useraddcern cmspopdb

sed -i "s@cmspopdb@$DASHBUSER@" /etc/cron.d/victor.agent.cms

changeOwner /opt/dq2/etc/dq2.cfg
changeOwner /opt/dq2/etc/logging.cfg
