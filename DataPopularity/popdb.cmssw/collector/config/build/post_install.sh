#!/bin/bash

function changeOwner(){
    [ ! -d $1  ] &&  mkdir -p $1 
    chown -R $DASHBUSER $1 
    echo 'chown for ' $1
}
# This is the user that will own the binaries
DASHBUSER=${DASHBUSER:=cmspopdb}
CMSSW_PORT=${CMSSW_PORT:=9331}
DASHB_NOTIFICATION=${DASHB_NOTIFICATION:=cms-popdb-alarms@cern.ch}

echo "User that will run the service is $DASHBUSER"
echo "Port for the UDP listener is ${CMSSW_PORT}"
echo "EMAIL notification address is ${DASHB_NOTIFICATION}"

#useradd --shell /bin/bash --create-home --home-dir /home/cern cern
/usr/sbin/useraddcern cmspopdb

changeOwner /opt/dashboard/etc/dashboard-simplevisor
changeOwner /opt/dashboard/var/messages
changeOwner /opt/dashboard/var/lock
changeOwner /opt/dashboard/var/log 
changeOwner /opt/dashboard/cron 

touch /opt/dashboard/var/log/dashboard-simplevisor.log
chmod 777 /opt/dashboard/var/log/dashboard-simplevisor.log

#comment cron, to be enabled after installation
sed -i 's@\(.*\)@#\1@' /etc/cron.d/dashboard_service_config
sed -i "s@dboard@$DASHBUSER@" /etc/cron.d/dashboard_service_config

sed -i "s@insert_CMSSW_PORT@${CMSSW_PORT}@" /opt/dashboard/etc/dashboard-service-config/service-config.xml

sed -i "s#dashboard-alarms@cern.ch#${DASHB_NOTIFICATION}#" /opt/dashboard/cron/dashbServices.sh
echo "In order to enable supervision of the process, uncomment cron line in script /etc/cron.d/dashboard_service_config"

