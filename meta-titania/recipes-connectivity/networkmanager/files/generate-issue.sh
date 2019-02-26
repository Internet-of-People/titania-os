#!/bin/bash

OLD_ISSUE_HASH=
if [[ -f /etc/issue ]]
then
    OLD_ISSUE_HASH="$(sha256sum /etc/issue)"
fi

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

NEW_ISSUE_HASH="$(sha256sum /etc/issue)"
if [[ $NEW_ISSUE_HASH != $OLD_ISSUE_HASH ]]
then
    # agetty will show the changed /etc/issue if killed with HUP signal.
    # If /etc/issue didn't change, no need to kill agetty.
    killall -HUP agetty
fi
