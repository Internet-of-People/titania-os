# Raspberry PI base image with splash and ssh
include recipes-core/images/rpi-basic-image.bb

IMAGE_INSTALL += "docker networkmanager"
