SUMMARY = "Data Partition image"
IMAGE_INSTALL = "docker-preinstall"
IMAGE_LINGUAS = ""
PACKAGE_INSTALL = "${IMAGE_INSTALL}"
IMAGE_FSTYPES = "ext3"

# Preventing overhead
IMAGE_CLASSES_remove = "sdcard_image-rpi"

# TODO: somehow suppress all POSTPROCESS
# initrd images probably should work as guidance

IMAGE_PREPROCESS_COMMAND += " datafs_cleanup; "

datafs_cleanup() {
    if test ! -d ${IMAGE_ROOTFS}; then
        echo "Image rootfs variable does not point to a directory"
        echo "IMAGE_ROOTFS=${IMAGE_ROOTFS}"
        exit 1
    fi

    rm -fr ${IMAGE_ROOTFS}${sysconfdir}
    rm -fr ${IMAGE_ROOTFS}${localstatedir}
    rm -fr ${IMAGE_ROOTFS}/run
}

inherit image
