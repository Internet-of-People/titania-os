DESCRIPTION = "SWupdate image for TitaniaOS on RaspberryPI3"

LICENSE = "GPL-3.0"

# https://sbabic.github.io/swupdate/building-with-yocto.html

SRC_URI = "file://sw-description \
           file://gplv3.md \
           file://postinst_loc_data_purge.sh \
           file://postinst_uboot_upgrade.sh \
           file://postinst_update_fstab.sh \
          "

LIC_FILES_CHKSUM = "file://${WORKDIR}/gplv3.md;md5=f149fa3bc39a974fe62c04649f34883a"

IMAGE_DEPENDS = "rpi-titania-image virtual/kernel"

SWUPDATE_IMAGES = "rpi-titania-image"
SWUPDATE_IMAGES_FSTYPES[rpi-titania-image] = ".ext4.gz"

SWUPDATE_IMAGES += " uImage"
SWUPDATE_IMAGES_FSTYPES[uImage] = ".bin"

SWUPDATE_IMAGES += " bcm2710-rpi-3-b"
SWUPDATE_IMAGES_FSTYPES[bcm2710-rpi-3-b] = ".dtb"
SWUPDATE_IMAGES_NOAPPEND_MACHINE[bcm2710-rpi-3-b] = "1"

SWUPDATE_IMAGES += " bcm2710-rpi-3-b-plus"
SWUPDATE_IMAGES_FSTYPES[bcm2710-rpi-3-b-plus] = ".dtb"
SWUPDATE_IMAGES_NOAPPEND_MACHINE[bcm2710-rpi-3-b-plus] = "1"

SWUPDATE_IMAGES += " u-boot"
SWUPDATE_IMAGES_FSTYPES[u-boot] = ".bin"
SWUPDATE_IMAGES_NOAPPEND_MACHINE[u-boot] = "1"

SWUPDATE_IMAGES += " boot"
SWUPDATE_IMAGES_FSTYPES[boot] = ".scr"
SWUPDATE_IMAGES_NOAPPEND_MACHINE[boot] = "1"

inherit swupdate
