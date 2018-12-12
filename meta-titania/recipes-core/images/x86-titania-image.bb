#!/bin/sh
LICENSE = "GPL-3.0"
LIC_FILES_CHKSUM = "file://LICENSE.md;md5=f149fa3bc39a974fe62c04649f34883a"

require titania-rootfs.inc

inherit x86img

##### Raspberry PI base image with splash and ssh
####include recipes-core/images/rpi-basic-image.bb
include recipes-core/images/core-image-minimal.bb

IMAGE_CLASSES += " x86img"

IMAGE_FEATURES += " ssh-server-dropbear "
# TODO +splash

IMAGE_INSTALL += " \
    kernel-modules \
"

##### Cause datafs image to be built
do_image_wic[depends] += "titania-datafs-image:do_build"

require titania-packages.inc
require user-setup.inc
require clean-logs.inc
require sync-clock.inc
require persistent.inc
require systemd-coma-dot.inc

# Inject additional partitions:
# - Second root of size ROOTFS_SIZE
# - Data partition of DATAFS_SIZE (extended to the end of the drive on the first run)
# TODO: maybe split DATA partition to a separate state partition
# but this requires either GPT (bad for bootloader on RPi) or
# an extended partition
# TODO: label datafs?
# TOOD: can we query that somehow?
DATAFS_FILENAME ?= "titania-datafs-image-${MACHINE}.ext4"
