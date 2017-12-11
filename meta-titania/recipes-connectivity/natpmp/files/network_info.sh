#!/bin/sh
# TODO: python?
# TODO: replace all that with that python lib?
# TODO: compile grep with PRCE and use lookaround instead of two greps
# sed is ugly

ROUTER_IP=$(natpmpc | grep -o 'Public IP.*$' | grep -o '[0-9.]*')
IPINFO=$(curl -s https://ipinfo.io)
EXTERNAL_IP=$(echo $IPINFO | grep -o '"ip": "[0-9.]*"' | grep -o '[0-9.]*')
LOCATION=$(echo $IPINFO | grep -o '"loc": "[0-9,.]*"' | grep -o '[0-9,.]*')

echo -e "Router reported address:\t$ROUTER_IP"
echo -e "Address seen from outside:\t$EXTERNAL_IP"

if [ "$ROUTER_IP" != "$EXTERNAL_IP" ] ; then
    echo "Router's declared IP does not match the public one"
    echo "Possibly the router is behind NAT, aborting operation"
    exit -1
fi

echo -e "Location:\t\t\t$LOCATION"

LATITUDE=$(echo $LOCATION | grep -o '^[0-9.]*')
LONGITUDE=$(echo $LOCATION | grep -o '[0-9.]*$')

# Should be the same as EXTERNAL_IP, right?
# TODO: race conditions when run in parallel a few times, do a HEREDOC or something
echo "PUBLIC_IP='$ROUTER_IP'" > /run/network_info.env
echo "LATITUDE='$LATITUDE'" >> /run/network_info.env
echo "LOGNITUDE='$LONGITUDE'" >> /run/network_info.env