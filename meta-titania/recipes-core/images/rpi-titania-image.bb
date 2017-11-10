# Raspberry PI base image with splash and ssh
include recipes-core/images/rpi-basic-image.bb

# TODO: migrate to python3 soon
IMAGE_INSTALL += "docker networkmanager python-core"
