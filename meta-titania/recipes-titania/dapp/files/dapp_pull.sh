#!/bin/bash
# If we still don't have an image, pull it
DOCKER_IMAGE_BASE=$(grep -o '^[^@]*'<<<$1)

if test -z "$(docker images -q $DOCKER_IMAGE_BASE)"; then
    echo "Downloading dApp image"
    docker pull $1 && docker tag $1 $DOCKER_IMAGE_BASE:latest
else
    echo "dApp image already downloaded"
fi