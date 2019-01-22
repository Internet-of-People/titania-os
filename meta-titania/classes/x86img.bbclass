inherit image_types
# Create a disk image that can be booted by kvm or converted to other formats like vmdk.

# The disk layout used is specified in titania-x86.wks
WKS_FILE = "titania-x86.wks"

# TODO this or extlinux should be used to run u-boot as a module
# so the original boot.scr can be used also on x86 platform
WKS_FILE_DEPENDS_BOOTLOADERS_x86-64 = "syslinux"

# This image depends on the rootfs image
IMAGE_TYPES = "wic"

# Set initramfs extension
KERNEL_INITRAMFS ?= ""

do_image_x86img[depends] = " \
    parted-native:do_populate_sysroot \
    mtools-native:do_populate_sysroot \
    dosfstools-native:do_populate_sysroot \
    virtual/kernel:do_deploy \
    titania-datafs-image:do_build \
"
# TODO FIXME bootloader?

do_image_x86img[recrdeps] = "do_build"

# Additional files and/or directories to be copied into the vfat partition from the IMAGE_ROOTFS.
FATPAYLOAD ?= ""

# SD card vfat partition image name
SDIMG_VFAT = "${IMAGE_NAME}.vfat"
SDIMG_LINK_VFAT = "${IMGDEPLOYDIR}/${IMAGE_LINK_NAME}.vfat"

