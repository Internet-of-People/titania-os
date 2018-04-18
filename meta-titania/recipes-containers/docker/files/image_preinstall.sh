#!/bin/sh

# TODO: figure out the exact extension with wildcards
IMAGE="/datafs/titania/docker/preinstall/$1.tar"

if test -f "$IMAGE" ; then
    echo "Loading $IMAGE into docker"

	docker load -i $IMAGE && rm -f $IMAGE
fi