#!/bin/bash

usage() {
    echo "Usage: forward_port.sh start|stop PORT-proto"
    exit 1
}

if test $# -lt 2; then
    usage
fi

case $1 in
    start)
        # That's a year (3600*24*365)
        DELAY=31536000
        ;;
    stop)
        DELAY=0
        ;;
    *)
        usage
esac

# TODO: maybe check the second argument for validity
natpmpc -a $(sed -e 's/\(.*\)-\(.*\)/\1 \1 \2/'<<<$2) $DELAY