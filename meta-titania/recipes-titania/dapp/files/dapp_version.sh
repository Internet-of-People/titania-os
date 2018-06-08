#!/bin/bash
# TODO: usage, error messages etc

# Determining image name
# TODO: maybe extract from json directly?
SYSTEMD_PATH="/run/systemd/system"
CONF_PATH="$SYSTEMD_PATH/dapp@$2.service.d/dapp.conf"
IMAGE_NAME=$(sed -ne 's/Environment=DAPP_DOCKER_IMAGE=\(.*\)$/\1/p' $CONF_PATH)
TAG_NAME=$(grep -o '^[^@]*'<<<$IMAGE_NAME)":latest"

# TODO: possibly simplify by extracting the hash part in the end
case "$1" in
    hub)
    # TODO: non sha256 hashes too?
    grep -o 'sha256.*$'<<<$IMAGE_NAME
    ;;

    # TODO: a much better name for here when we go Mercury?
    # TODO: hardcoding 'latest'
    docker)
    manifest-tool inspect $TAG_NAME | sed -ne 's/^ *Digest: \(sha256:[0-9a-f]*\)/\1/p'
    ;;

    image)
    docker image inspect $TAG_NAME --format='{{ index .RepoDigests 0 }}' | grep -o 'sha256:.*$'
    ;;

    dapp)
    docker inspect $2 --format='{{ .Config.Image }}' | grep -o 'sha256:.*$'
    ;;

    *)
    echo "Wrong command $1"
    exit 1
    ;;
esac