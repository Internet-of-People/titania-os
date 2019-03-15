#!/bin/bash
# Open up ports on the router via natpmp for the public ports

if [[ $1 != "start" && $1 != "stop" ]]
then
    echo "Usage: $0 [start|stop] <dapp_name>"
    exit 1
fi

if [[ -z $2 ]]
then
    echo "dapp name must be specified"
    exit 1
fi

ACTION=$1
DAPP_ID=$2

function public_ports()
{
    local DAPP_ID_=$1
    local PROTOCOL=$2

    jq ".[] | select(.id == \"$DAPP_ID_\") | .ports | .[] | select(.type == \"public\") | select(.protocol == \"$PROTOCOL\") | .port" /run/apps.json
}

case $ACTION in
    start)
        echo "Setting up portforwarding via natpmp for public ports."
        for typ in tcp udp
        do
            for port in $(public_ports $DAPP_ID $typ)
            do
                echo Setting up $typ portforward on port $port
                systemctl start forward-port@${port}-${typ}.service || true  # service fails if natpmp is not enabled on router
            done
        done
        ;;

    stop)
        echo "Removing natpmp portforwards"
        for typ in tcp udp
        do
            for port in $(public_ports $DAPP_ID $typ)
            do
                echo Removing $typ portforward from port $port
                systemctl stop forward-port@${port}-${typ}.service || true  # service fails if natpmp is not enabled on router
            done
        done
        ;;

    *)
        echo "start/stop command must be specified"
        exit 1
        ;;
esac
