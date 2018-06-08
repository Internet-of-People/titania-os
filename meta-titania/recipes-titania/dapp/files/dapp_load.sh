#!/bin/bash
# If there is a file, import
# TODO: threat model assumes attackers won't be able to write there unless they are root
DOCKER_IMAGE_BASE_NAME=$(grep -o '^[^@:]*'<<<$1)
DOCKER_IMAGE_FILE=/var/lib/docker/preinstall/$(echo $DOCKER_IMAGE_BASE_NAME | tr '/' '_').tar

if test -f "$DOCKER_IMAGE_FILE"; then
    echo "Loading dApp image"
    docker load -i "$DOCKER_IMAGE_FILE" && \
        rm -f "$DOCKER_IMAGE_FILE" && \
        docker tag $1 ${DOCKER_IMAGE_BASE_NAME}:latest
else
    echo "dApp pre-downloaded image not found"
fi