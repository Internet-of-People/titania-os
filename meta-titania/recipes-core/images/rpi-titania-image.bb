# Raspberry PI base image with splash and ssh
include recipes-core/images/rpi-basic-image.bb

# Monitoring backend
# TODO: migrate to python3 soon
IMAGE_INSTALL += "vuedj"

IMAGE_INSTALL += "docker networkmanager avahi-daemon"


