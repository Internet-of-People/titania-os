#!/bin/sh
DAPP_DOCKER_IMAGE_FILE=$1
shift
DAPP_DOCKER_CONTAINER_NAME=$1
shift

# If there is a file, import
# TODO: threat model assumes attackers won't be able to write there unless they are root
if test -f "$DAPP_DOCKER_IMAGE_FILE"; then
	docker load -i "$DAPP_DOCKER_IMAGE_FILE" && rm -f "$DAPP_DOCKER_IMAGE_FILE"
fi

# If there is no container, create
if ! docker inspect "$DAPP_DOCKER_CONTAINER_NAME" >/dev/null 2>&1; then
	docker create --name "$DAPP_DOCKER_CONTAINER_NAME" \
    --env-file /run/network_info.env \
    $*
fi
