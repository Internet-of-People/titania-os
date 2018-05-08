#!/bin/sh
# If there is a file, import
# TODO: threat model assumes attackers won't be able to write there unless they are root
if test -f "$2"; then
    echo "Loading dApp image"
    docker load -i "$2" && rm -f "$2"
else
    echo "dApp pre-downloaded image not found"
fi