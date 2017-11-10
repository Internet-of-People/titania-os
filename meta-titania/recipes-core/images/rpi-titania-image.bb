# Raspberry PI base image with splash and ssh
include recipes-core/images/rpi-basic-image.bb

# Python and friends for monitoring
# TODO: migrate to python3 soon
# TODO: remove after we move to rust (don't forget to remove the layer too)
IMAGE_INSTALL += "python-core python-pip python-django python-pytz python-djangorestframework"

IMAGE_INSTALL += "docker networkmanager"


