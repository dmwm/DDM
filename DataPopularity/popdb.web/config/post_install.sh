#!/bin/bash

function changeOwner(){
    [ ! -d $1  ] &&  mkdir -p $1 
    chown -R $DASHBUSER $1 
    echo 'chown for ' $1
}
# This is the user that will own the binaries
DASHBUSER=${DASHBUSER:=apache}
DASHB_NOTIFICATION=${DASHB_NOTIFICATION:=cms-popdb-alarms@cern.ch}

echo "User that will run the service is $DASHBUSER"
echo "Port for the UDP listener is ${CMSSW_PORT}"
echo "EMAIL notification address is ${DASHB_NOTIFICATION}"

#useradd --shell /bin/bash --create-home --home-dir /home/cern cern
#/usr/sbin/useraddcern cmspopdb

changeOwner /var/www/DjangoProjects/CMSDataPopularity/cache
changeOwner /var/www/DjangoProjects/CMSDataPopularity/logs


