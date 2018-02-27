#!/bin/sh

# TODO: figure out the exact extension with wildcards
IMAGE="/datafs/docker/preinstall/$1.tar.gz"

if test -f "$IMAGE" ; then
    echo "Loading $IMAGE into docker"

	docker load -i $IMAGE && rm -f $IMAGE
fi