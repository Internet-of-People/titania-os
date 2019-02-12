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

# Must specify rootfs size, which actually means the minimum size of it.
# The size in the .wks file is for the partition only.
# Overhead factor must be specified to override the default 1.3.
# The default behaviour is to make partition that is bigger than its contents by the overhead factor.
IMAGE_ROOTFS_SIZE = "516096"
IMAGE_OVERHEAD_FACTOR = "1"
IMAGE_ROOTFS_MAXSIZE = "516096"
