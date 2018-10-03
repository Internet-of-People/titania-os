#!/bin/sh
# TODO: python?
# TODO: replace all that with that python lib?
# TODO: compile grep with PRCE and use lookaround instead of two greps
# sed is ugly

NETWORK_INFO_FILE="/run/network_info.env"

# Put the file on disk not to abort docker containers
# TODO: better way to inform the containers
touch $NETWORK_INFO_FILE

# Retries before giving up
RETRY_AMOUNT=10
# Time in seconds to wait between each retry
RETRY_COOLDOWN=2

# Touch the file just in case
for i in $(seq 1 $RETRY_AMOUNT); do
    IPINFO=$(curl -s https://ipinfo.io)
    LOCATION=$(echo $IPINFO | grep -o '"loc": "[0-9,.-]*"' | grep -o '[0-9,.-]*')


    LATITUDE=$(echo $LOCATION | grep -o '^[0-9.-]*')
    LONGITUDE=$(echo $LOCATION | grep -o '[0-9.-]*$')

    EXTERNAL_IP=$(echo $IPINFO | grep -o '"ip": "[0-9.]*"' | grep -o '[0-9.]*')

    # Check if we get everything correctly
    if test -n "$LATITUDE" -a -n "$LONGITUDE" -a -n "$EXTERNAL_IP"; then
        break
    elif test $i -ge "$RETRY_AMOUNT"; then
        echo "Can not learn the network environment"
        exit -1
    fi

    sleep $RETRY_COOLDOWN
done

echo -e "Location:\t\t\t$LOCATION"
echo -e "Latitude:\t$LATITUDE"
echo -e "Longitude:\t$LONGITUDE"
echo -e "Address seen from outside:\t$EXTERNAL_IP"


# TODO: TYO-19, change to whatever ssl library we end up using
HMAC="titania"
SSH_KEY="/etc/dropbear/dropbear_rsa_host_key"
NODEID="$(dropbearkey -y -f $SSH_KEY | sed -ne 's/^ssh-rsa \([^ ]*\).*$/\1/p' | openssl sha1 -r -hmac $HMAC | cut -d' ' -f1)"
echo "SSH-based node ID: $NODEID"
echo "NODEID=$NODEID" > $NETWORK_INFO_FILE

# TODO: race conditions when run in parallel a few times, do a HEREDOC or something
echo "PUBLIC_IP=$EXTERNAL_IP" >> $NETWORK_INFO_FILE
echo "LATITUDE=$LATITUDE" >> $NETWORK_INFO_FILE
echo "LONGITUDE=$LONGITUDE" >> $NETWORK_INFO_FILE

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
else
    echo "We seem to be directly connected to the internet"
    # TODO: do we need to mark it?
fi
