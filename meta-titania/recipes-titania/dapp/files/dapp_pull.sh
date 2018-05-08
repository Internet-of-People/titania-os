#!/bin/sh
# If we still don't have an image, pull it
if test -z "$(docker images -q $2)"; then
    echo "Downloading dApp image"
    docker pull $2
else
    echo "dApp image already downloaded"
fi