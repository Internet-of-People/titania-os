#!/bin/sh

# If there is no container, create
if ! docker inspect "$1" >/dev/null 2>&1; then
    echo "Creating dApp container"
    # Getting the detailed image name
    IMAGE_NAME="$(/opt/titania/bin/dapp_version.sh image $1)"
    IMAGE_DIGEST="$(/opt/titania/bin/dapp_version.sh digest $1)"

    if [[ -n $IMAGE_DIGEST ]]
    then
        IMAGE_SPEC="${IMAGE_NAME}@${IMAGE_HASH}"
    else
        IMAGE_SPEC="${IMAGE_NAME}"
    fi

    echo "Full image name: ${IMAGE_SPEC}"

    # Directory for exchanging static files with nginx
    # - shared allows bind mount to propagate
    EXTRA_VOLUMES="-v /run/dapp/$1:/dapp:shared"

    # -it needed for global.iop.ps
    docker create -it $EXTRA_VOLUMES --env-file /run/network_info.env --name $* ${IMAGE_SPEC}
else
    echo "dApp container already present"
fi
