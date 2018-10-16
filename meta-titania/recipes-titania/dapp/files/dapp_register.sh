#!/bin/bash
# Utility to create per-dapp http(s) forwards
# TODO: make configurable
# TODO: /dapp directory is hardcoded
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
    # TODO: no slash at the end removes automatic redirect feature (e.g. /user to /user/)
    # refer to nginx docu how to fix it if needed
    # TODO: allowing try_files to probe directories results in 403 when a listing is
    # to be generated. Current solution prevents implicit directory indexes (e.g. index.html)
    # from being statically served, write a workaround if needed
    cat > $DAPP_CONF_PATH/$DAPP_ID.conf <<EOF
location /dapp/$DAPP_ID {
    rewrite ^/dapp/$DAPP_ID/?(.*)\$ /\$1 break;
    root /dapp_assets/$DAPP_ID/;
    try_files \$uri @$DAPP_ID;
}

location @$DAPP_ID {
    proxy_pass http://$IP;
    proxy_set_header X-Forwarded-Proto \$scheme;
    proxy_set_header Host \$http_host;
}
EOF

    # Mount static files directory
    if test -n "$3"; then
        PID=$(docker inspect --format {{.State.Pid}} $DAPP_ID)
        # No need to retry, should be up by now
        if test -z "$PID"; then
            # TODO: WARNING: a malicious app developer can mount system devices
            # Prevent this by checking that $3 is a valid path (in next commit)
            nsenter --target $PID --mount --uts --ipc --net --pid -- \
                mount -o bind,ro $3 /dapp 
        fi 
    fi
    ;;

    stop)
    echo "Removing nginx drop-in config"
    rm -f $DAPP_CONF_PATH/$DAPP_ID.conf

    # TODO: study if we should unmount the static directory
    ;;

    *)
    echo "start/stop command must be specified"
    exit -1
    ;;
esac

# Reload nginx config
# TODO: should this be done in systemd unit instead?
systemctl reload dapp@world.libertaria.nginx
