#!/bin/sh

NETWORK_INFO_FILE="/run/network_info.env"

HMAC="titania"
SSH_KEY="/etc/dropbear/dropbear_rsa_host_key"
NODEID="$(dropbearkey -y -f $SSH_KEY | sed -ne 's/^ssh-rsa \([^ ]*\).*$/\1/p' | openssl sha1 -r -hmac $HMAC | cut -d' ' -f1)"
echo "SSH-based node ID: $NODEID"
echo "NODEID=$NODEID" > $NETWORK_INFO_FILE

# Time in seconds to wait between each retry
RETRY_COOLDOWN=2

while true
do
    IPINFO=$(curl -s https://ipinfo.io)

    if [[ $? = 0 ]]
    then
        LOCATION=$(echo $IPINFO | grep -o '"loc": "[0-9,.-]*"' | grep -o '[0-9,.-]*')
        LATITUDE=$(echo $LOCATION | grep -o '^[0-9.-]*')
        LONGITUDE=$(echo $LOCATION | grep -o '[0-9.-]*$')

        EXTERNAL_IP=$(echo $IPINFO | grep -o '"ip": "[0-9.]*"' | grep -o '[0-9.]*')

        # Check if we get everything correctly
        if test -n "$LATITUDE" -a -n "$LONGITUDE" -a -n "$EXTERNAL_IP"; then
            break
        fi
    fi

    sleep $RETRY_COOLDOWN
done

echo -e "Location:\t\t\t$LOCATION"
echo -e "Latitude:\t$LATITUDE"
echo -e "Longitude:\t$LONGITUDE"
echo -e "Address seen from outside:\t$EXTERNAL_IP"

echo "PUBLIC_IP=$EXTERNAL_IP" >> $NETWORK_INFO_FILE
echo "LATITUDE=$LATITUDE" >> $NETWORK_INFO_FILE
echo "LONGITUDE=$LONGITUDE" >> $NETWORK_INFO_FILE

# Check if we need to reload LOC with the new coordinates
if ! docker inspect global.iop.loc --format='{{ Config.Env }}' | grep -q "LATITUDE=."
then
    # recreate container with the new location
    systemctl stop dapp@global.iop.loc.service
    docker rm -f global.iop.loc
    systemctl start dapp@global.iop.loc.service
fi

if /sbin/ifconfig | grep -vq "addr:${EXTERNAL_IP}" ; then
    echo "We seem to be behind the router, trying NAT-PMP"

    ROUTER_IP=$(natpmpc | grep -o 'Public IP.*$' | grep -o '[0-9.]*')
    if [ -z "$ROUTER_IP" ]; then
        echo "Router either doesn't support NAT-PMP or does not allow us to see its IP"
        exit -1
    else
        echo -e "Router reported address:\t$ROUTER_IP"
    fi

    echo "ROUTER_IP=$ROUTER_IP" >> $NETWORK_INFO_FILE

    if [ "$ROUTER_IP" != "$EXTERNAL_IP" ] ; then
        echo "Router's declared IP does not match the public one"
        echo "Possibly the router is behind NAT, aborting operation"
        exit -1
    fi
fi

