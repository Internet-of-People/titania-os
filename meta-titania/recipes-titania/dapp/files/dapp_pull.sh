#!/bin/sh
# If we still don't have an image, pull it
if test -z "$(docker images -q $1)"; then
    echo "Downloading dApp image"
    docker pull $1
else
    echo "dApp image already downloaded"
fi