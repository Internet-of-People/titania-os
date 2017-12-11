#!/bin/sh
# TODO: python?
# TODO: replace all that with that python lib?
# TODO: compile grep with PRCE and use lookaround instead of two greps
# sed is ugly

IPINFO=$(curl -s https://ipinfo.io)
LOCATION=$(echo $IPINFO | grep -o '"loc": "[0-9,.]*"' | grep -o '[0-9,.]*')
echo -e "Location:\t\t\t$LOCATION"

EXTERNAL_IP=$(echo $IPINFO | grep -o '"ip": "[0-9.]*"' | grep -o '[0-9.]*')
echo -e "Address seen from outside:\t$EXTERNAL_IP"

if /sbin/ifconfig | grep -vq "addr:${EXTERNAL_IP}" ; then
    echo "We seem to be behind the router, trying NAT-PMP"

    ROUTER_IP=$(natpmpc | grep -o 'Public IP.*$' | grep -o '[0-9.]*')
    echo -e "Router reported address:\t$ROUTER_IP"

    if [ "$ROUTER_IP" != "$EXTERNAL_IP" ] ; then
        echo "Router's declared IP does not match the public one"
        echo "Possibly the router is behind NAT, aborting operation"
        exit -1
    fi
else
    echo "We seem to be directly connected to the internet"
fi

LATITUDE=$(echo $LOCATION | grep -o '^[0-9.]*')
LONGITUDE=$(echo $LOCATION | grep -o '[0-9.]*$')

# TODO: race conditions when run in parallel a few times, do a HEREDOC or something
echo "PUBLIC_IP='$EXTERNAL_IP'" > /run/network_info.env
echo "LATITUDE='$LATITUDE'" >> /run/network_info.env
echo "LOGNITUDE='$LONGITUDE'" >> /run/network_info.env