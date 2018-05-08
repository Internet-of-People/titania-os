#!/bin/sh
# If there is no container, create
if ! docker inspect "$1" >/dev/null 2>&1; then
    echo "Creating dApp container"
    # -it needed for global.iop.ps TODO: standardize
    docker create -it --env-file /run/network_info.env --name $*
else
    echo "dApp container already present"
fi
