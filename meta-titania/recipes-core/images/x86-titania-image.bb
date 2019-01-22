#!/bin/sh
LICENSE = "GPL-3.0"
LIC_FILES_CHKSUM = "file://LICENSE.md;md5=f149fa3bc39a974fe62c04649f34883a"

require titania-rootfs.inc

inherit x86img

include recipes-core/images/core-image-minimal.bb

IMAGE_CLASSES += " x86img"

IMAGE_FEATURES += " ssh-server-dropbear "
# TODO +splash

IMAGE_INSTALL += " \
    kernel-modules \
"

require titania-datafs.inc
require titania-packages.inc
require user-setup.inc
require clean-logs.inc
require sync-clock.inc
require persistent.inc
require systemd-coma-dot.inc
