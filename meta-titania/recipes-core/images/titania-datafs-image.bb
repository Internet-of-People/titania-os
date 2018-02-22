SUMMARY = "Data Partition image"
IMAGE_INSTALL = "docker-preinstall"
IMAGE_LINGUAS = ""
PACKAGE_INSTALL = "${IMAGE_INSTALL}"
IMAGE_FSTYPES = "ext3"

# Preventing overhead
IMAGE_CLASSES_remove = "sdcard_image-rpi"

inherit image
