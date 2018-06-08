#!/bin/bash
# If there is a file, import
# TODO: threat model assumes attackers won't be able to write there unless they are root
DOCKER_IMAGE_FILE=/var/lib/docker/preinstall/$(echo $1 | tr '/:@' '___').tar

if test -f "$DOCKER_IMAGE_FILE"; then
    echo "Loading dApp image"
    docker load -i "$DOCKER_IMAGE_FILE" && \
        rm -f "$DOCKER_IMAGE_FILE" && \
        docker tag $1 $(grep -o '^[^@]*'<<<$1):latest
else
    echo "dApp pre-downloaded image not found"
fi