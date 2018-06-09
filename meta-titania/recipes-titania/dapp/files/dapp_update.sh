#!/bin/bash

# TODO: offline operation
# TODO: bad argument checks

# Usage: ./dapp_update.sh <dapp> [-n]

# If -n is specified (only as a past argument), print the action
# to be done instead, don't actually do anything.

# Possible outcomes:
# - "latest" = everything is matching JSON
# - "download" = JSON points at a differing version, needs download
#   - NOTE: if the user has the container at latest
#       but manages to somehow downgrade the image, it's not
#       our problem
# - "create" = image is at JSON version, there is no container 
# - "recreate" = image is at JSON version, container needs to be recreated

# Add custom commands to PATH
PATH=$PATH:/opt/titania/bin

# Mark if we need a dry run
if test "$2" == "-n"; then
    DRY_RUN="yes"
fi 

dry_run() {
    if test -n "$DRY_RUN"; then
        echo $1
        exit 0
    fi
}

JSON_VERSION=$(dapp_version.sh hub $1)
IMAGE_VERSION=$(dapp_version.sh image $1)

# We need to download
if test "$JSON_VERSION" != "$IMAGE_VERSION"; then
    dry_run "download"
    # TODO: what if we change the repo name?
    BASE_IMAGE="$(dapp_version.sh base $1)"

    # May fail
    (docker tag ${BASE_IMAGE}:latest ${BASE_IMAGE}:previous 2>&1 >/dev/null) || true
    
    docker pull ${BASE_IMAGE}@${JSON_VERSION} 
    docker tag ${BASE_IMAGE}@${JSON_VERSION} ${BASE_IMAGE}:latest
fi

# No container yet
if ! docker inspect $1 >/dev/null 2>&1; then
    dry_run "create"
    # TODO: check for broken conditions, e.g. service
    # is started, but the container is removed etc
    # Note: implicitly starts
    systemctl start dapp@$1
else
    DAPP_VERSION=$(dapp_version.sh dapp $1)
    if test "$JSON_VERSION" != "$DAPP_VERSION"; then
        dry_run "recreate"
        systemctl stop dapp@$1
        docker rm $1
        systemctl start dapp@$1
    fi
fi 

dry_run "latest"