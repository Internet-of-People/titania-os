# Common rootfs related settings
require titania-rootfs.inc

# Base image with splash
include recipes-core/images/core-image-base.bb

require titania-packages.inc
require titania-datafs.inc
require user-setup.inc
require clean-logs.inc
require sync-clock.inc
require persistent.inc
require systemd-coma-dot.inc

WKS_FILE = "titania-rpi.wks"
IMAGE_INSTALL += "swupdate"
