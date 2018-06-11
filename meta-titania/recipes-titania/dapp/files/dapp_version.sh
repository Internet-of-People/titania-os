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

# TODO: possibly simplify by extracting the hash part in the end
case "$1" in
    latest)
    manifest-tool inspect $IMAGE_NAME | sed -ne 's/^ *Digest: \(sha256:[0-9a-f]*\)/\1/p'
    ;;

    image)
    DIGEST_DIR=/var/lib/docker/preinstall
    DIGEST_FILE="$(grep -o '^[^:@]*'<<<$IMAGE_NAME | tr '/' '_').digest"
    # Try the image, then try a file. then fail
    (docker image inspect $IMAGE_NAME --format='{{ index .RepoDigests 0 }}' 2>/dev/null | grep -o 'sha256:.*$') || \
    cat $DIGEST_DIR/$DIGEST_FILE 2>/dev/null ||
    echo "nil"
    ;;

    dapp)
    (docker inspect $2 --format='{{ .Config.Image }}' 2>/dev/null | grep -o 'sha256:.*$' ) || echo "nil"
    ;;

    base)
    echo $IMAGE_NAME
    ;;

    *)
    echo "Wrong command $1"
    exit 1
    ;;
esac