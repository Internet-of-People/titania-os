DESCRIPTION = "SWupdate image for TitaniaOS on RaspberryPI3"

LICENSE = "GPL-3.0"

# https://sbabic.github.io/swupdate/building-with-yocto.html

SRC_URI = "file://sw-description\
           file://gplv3.md"

LIC_FILES_CHKSUM = "file://${WORKDIR}/gplv3.md;md5=f149fa3bc39a974fe62c04649f34883a"

IMAGE_DEPENDS = "rpi-titania-image virtual/kernel"

SWUPDATE_IMAGES = "rpi-titania-image uImage"
SWUPDATE_IMAGES_FSTYPES[rpi-titania-image] = ".ext4.gz"
SWUPDATE_IMAGES_FSTYPES[uImage] = ".bin"

inherit swupdate
