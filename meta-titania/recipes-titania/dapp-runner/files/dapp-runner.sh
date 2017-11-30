#!/bin/sh

CONTAINER_NAME=$(echo $1 | tr ',' '\n' | sed '1!d')
ACCOUNT_NAME=$(echo $1 | tr ',' '\n' | sed '2!d')
IMAGE_NAME=$(echo $1 | tr ',' '\n' | sed '3!d')

# If only two are given, treat the last as image name
if [ -z $IMAGE_NAME ]; then
    IMAGE_SPEC=$ACCOUNT_NAME
else
    IMAGE_SPEC=$ACCOUNT_NAME/$IMAGE_NAME
fi

# Create if needed
if ! docker inspect $CONTAINER_NAME >/dev/null 2>&1; then
    echo "[dapp-runner] No previously created container found, making a new one"
    # TODO: volumes
    docker create --name $CONTAINER_NAME $IMAGE_SPEC
fi

# Run the containe
docker start -a $CONTAINER_NAME