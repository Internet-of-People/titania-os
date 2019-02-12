#!/bin/bash

cat /etc/titania.ascii > /etc/issue

IPS=$(ip -4 addr show | grep -w inet | grep -vw lo | grep -wv docker0 | awk '{print $2}' | cut -d/ -f1)
if [[ $? = 0 ]]
then
	for IP in $IPS
	do
	    echo -e "\t\t\tTitania Web Interface:  http://$IP/" >> /etc/issue
	done
fi

echo >> /etc/issue
cat /etc/issue.titania >> /etc/issue

killall -HUP agetty
