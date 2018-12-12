inherit image_types

#
# Create an image that can be written onto a SD card using dd.
#
# The disk layout used is:
#
#    0                      -> IMAGE_ROOTFS_ALIGNMENT         - reserved for other data
#    IMAGE_ROOTFS_ALIGNMENT -> BOOT_SPACE                     - bootloader and kernel
#    BOOT_SPACE             -> SDIMG_SIZE                     - rootfs
#

#                                                     Default Free space = 1.3x
#                                                     Use IMAGE_OVERHEAD_FACTOR to add more space
#                                                     <--------->
#            4MiB              40MiB           SDIMG_ROOTFS
# <-----------------------> <----------> <---------------------->
#  ------------------------ ------------ ------------------------
# | IMAGE_ROOTFS_ALIGNMENT | BOOT_SPACE | ROOTFS_SIZE            |
#  ------------------------ ------------ ------------------------
# ^                        ^            ^                        ^
# |                        |            |                        |
# 0                      4MiB     4MiB + 40MiB       4MiB + 40Mib + SDIMG_ROOTFS

WKS_FILE = "titania-x86.wks"

# TODO this or extlinux should be used to run u-boot as a module
# so the original boot.scr can be used also on x86 platform
WKS_FILE_DEPENDS_BOOTLOADERS_x86-64 = "syslinux"

# This image depends on the rootfs image
IMAGE_TYPEDEP_x86img = "${SDIMG_ROOTFS_TYPE}"
IMAGE_TYPES = "wic"

# Set initramfs extension
KERNEL_INITRAMFS ?= ""

SDIMG_KERNELIMAGE = "kernel7.img"

# Kernel image name
#SDIMG_KERNELIMAGE_raspberrypi  ?= "kernel.img"
#SDIMG_KERNELIMAGE_raspberrypi2 ?= "kernel7.img"
#SDIMG_KERNELIMAGE_raspberrypi3-64 ?= "kernel8.img"

# Boot partition size [in KiB] (will be rounded up to IMAGE_ROOTFS_ALIGNMENT)
BOOT_SPACE ?= "40960"

# Set alignment to 4MB [in KiB]
IMAGE_ROOTFS_ALIGNMENT = "4096"

# Use an uncompressed ext3 by default as rootfs
SDIMG_ROOTFS_TYPE ?= "ext3"
SDIMG_ROOTFS = "${IMGDEPLOYDIR}/${IMAGE_LINK_NAME}.${SDIMG_ROOTFS_TYPE}"

do_image_x86img[depends] = " \
			parted-native:do_populate_sysroot \
			mtools-native:do_populate_sysroot \
			dosfstools-native:do_populate_sysroot \
			virtual/kernel:do_deploy \
            titania-datafs-image:do_build \
			"


#			u-boot:do_deploy \
#			${IMAGE_BOOTLOADER}:do_deploy \
# TODO FIXME bootloader?

do_image_x86img[recrdeps] = "do_build"

# Compression method to apply to SDIMG after it has been created. Supported
# compression formats are "gzip", "bzip2" or "xz". The original .lezimg file
# is kept and a new compressed file is created if one of these compression
# formats is chosen. If SDIMG_COMPRESSION is set to any other value it is
# silently ignored.
#SDIMG_COMPRESSION ?= ""

# Additional files and/or directories to be copied into the vfat partition from the IMAGE_ROOTFS.
FATPAYLOAD ?= ""

# SD card vfat partition image name
SDIMG_VFAT = "${IMAGE_NAME}.vfat"
SDIMG_LINK_VFAT = "${IMGDEPLOYDIR}/${IMAGE_LINK_NAME}.vfat"

def split_overlays(d, out, ver=None):
    dts = d.getVar("KERNEL_DEVICETREE")
    if out:
        overlays = oe.utils.str_filter_out('\S+\-overlay\.dtb$', dts, d)
        overlays = oe.utils.str_filter_out('\S+\.dtbo$', overlays, d)
    else:
        overlays = oe.utils.str_filter('\S+\-overlay\.dtb$', dts, d) + \
                   " " + oe.utils.str_filter('\S+\.dtbo$', dts, d)

    return overlays

