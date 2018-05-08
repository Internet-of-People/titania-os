#!/bin/sh
DAPP_DOCKER_CONTAINER_NAME=$1
shift
# If there is no container, create
if ! docker inspect "$DAPP_DOCKER_CONTAINER_NAME" >/dev/null 2>&1; then
    echo "Creating dApp container"
    # -it needed for global.iop.ps TODO: standardize
    docker create -it --name "$DAPP_DOCKER_CONTAINER_NAME" \
    --env-file /run/network_info.env \
    $*
else
    echo "dApp container already present"
fi
