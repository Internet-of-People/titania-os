#!/bin/bash
# Utility to create per-dapp http(s) forwards
# TODO: make configurable
DAPP_CONF_PATH="/run/dapp.conf.d/"
NGINX_SERVICE="dapp@world.libertaria.nginx"

if test -z "$2"; then
    echo "dapp name must be specified"
    exit -1
fi
DAPP_ID=$2

case $1 in
    start)
    echo "Creating nginx drop-in config"
    # 10 tries spaced at 1 second while the container starts up
    for i in $(seq 1 10); do
        IP=$(docker inspect -f '{{.NetworkSettings.IPAddress }}' $DAPP_ID)

        if test -n "$IP"; then 
            break 
        fi
        sleep 1
    done
    if test -z "$IP"; then 
        echo "Can not determine the container IP, aborting"
        exit -1
    fi 

    # TODO: currently only http, add https when we have it
    cat > $DAPP_CONF_PATH/$DAPP_ID.conf <<EOF
location /dapp/$DAPP_ID/ {
    proxy_pass http://$IP/;
EOF
    cat >> $DAPP_CONF_PATH/$DAPP_ID.conf <<'EOF'
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header Host $http_host;
}
EOF
    ;;

    stop)
    echo "Removing nginx drop-in config"
    rm -f $DAPP_CONF_PATH/$DAPP_ID.conf
    ;;

    *)
    echo "start/stop command must be specified"
    exit -1
    ;;
esac

# Reload nginx config
# TODO: should this be done in systemd unit instead?
systemctl reload dapp@world.libertaria.nginx