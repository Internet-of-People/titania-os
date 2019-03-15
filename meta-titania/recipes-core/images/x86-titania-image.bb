require titania-rootfs.inc

inherit x86img

include recipes-core/images/core-image-minimal.bb

IMAGE_CLASSES += "x86img"

IMAGE_FEATURES += "ssh-server-dropbear"

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
