#!/bin/bash

# Determining image name
SYSTEMD_PATH="/run/systemd/system"
CONF_PATH="$SYSTEMD_PATH/dapp@$2.service.d/dapp.conf"

if test ! -f "$CONF_PATH"; then
    echo "no dapp"
    exit 1
fi 

IMAGE_NAME=$(sed -ne 's/Environment=DAPP_DOCKER_IMAGE=\(.*\)$/\1/p' $CONF_PATH)

case "$1" in
    latest)
        manifest-tool inspect $IMAGE_NAME | sed -ne 's/^ *Digest: \(sha256:[0-9a-f]*\)/\1/p'
        ;;

    digest)
        # Return the digest of docker image, empty if digest is missing, error if image doesn't exist.
        # Try the image, then try a file. then fail
        (docker image inspect $IMAGE_NAME --format='{{ index .RepoDigests 0 }}' 2>/dev/null | grep -o 'sha256:.*$') || \
        exit 1
        ;;

    saved_digest)
        # Return the digest of preinstalled docker image
        DIGEST_DIR=/var/lib/docker/preinstall
        DIGEST_FILE="$(grep -o '^[^:@]*'<<<$IMAGE_NAME | tr '/' '_').digest"
        if [[ -f $DIGEST_DIR/$DIGEST_FILE ]]
        then
            cat $DIGEST_DIR/$DIGEST_FILE
        else
            exit 1
        fi
        ;;

    dapp)
        (docker inspect $2 --format='{{ .Config.Image }}' 2>/dev/null | grep -o 'sha256:.*$' ) || exit 1
        ;;

    image)
        # Return docker image name
        echo $IMAGE_NAME
        ;;

    *)
        echo "Wrong command $1"
        exit 1
        ;;
esac