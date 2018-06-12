#!/bin/bash
# If we still don't have an image, pull it
# Note this wiill not auto-update stuff
if test -z "$(docker images -q $1)"; then
    echo "Downloading dApp image"
    DOCKER_IMAGE_BASE=$(grep -o '^[^@:]*'<<<$1)
    
    docker pull $1 && docker tag $1 $DOCKER_IMAGE_BASE:latest && 
        rm -f /var/lib/docker/preinstall/$(echo $DOCKER_IMAGE_BASE | tr '/' '_').digest
else
    echo "dApp image already downloaded"
fi