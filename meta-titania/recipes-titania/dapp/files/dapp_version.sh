#!/bin/bash
# TODO: usage, error messages etc

# Determining image name
# TODO: maybe extract from json directly?
# TODO: should we be more verebose than 'nil'?
SYSTEMD_PATH="/run/systemd/system"
CONF_PATH="$SYSTEMD_PATH/dapp@$2.service.d/dapp.conf"

if test ! -f "$CONF_PATH"; then
    echo "no dapp"
    exit 1
fi 

IMAGE_NAME=$(sed -ne 's/Environment=DAPP_DOCKER_IMAGE=\(.*\)$/\1/p' $CONF_PATH)
IMAGE_BASE=$(grep -o '^[^@]*'<<<$IMAGE_NAME)
TAG_NAME=$IMAGE_BASE":latest"

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
    (docker image inspect $TAG_NAME --format='{{ index .RepoDigests 0 }}' 2>/dev/null | grep -o 'sha256:.*$') || echo "nil"
    ;;

    dapp)
    (docker inspect $2 --format='{{ .Config.Image }}' 2>/dev/null | grep -o 'sha256:.*$' ) || echo "nil"
    ;;

    base)
    echo $IMAGE_BASE
    ;;

    *)
    echo "Wrong command $1"
    exit 1
    ;;
esac