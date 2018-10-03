SUMMARY = "Data Partition image"
IMAGE_INSTALL = "dapp-preinstall base-files-datafs"
IMAGE_LINGUAS = ""
PACKAGE_INSTALL = "${IMAGE_INSTALL}"
# We only need ext4, nothing else
IMAGE_FSTYPES = "ext4"

# TODO: somehow suppress all POSTPROCESS
# initrd images probably should work as guidance

IMAGE_PREPROCESS_COMMAND += " datafs_cleanup; "

# Suppress prelink
IMAGE_PREPROCESS_COMMAND_remove = "prelink_setup;"
IMAGE_PREPROCESS_COMMAND_remove = "prelink_image;"
# TODO: use USER_CLASSES to remove image-prelink class instead
# This may affect normal images too

# Rationale: We use online resize so that by the time
# Docker will be preinstalling the images, the odds are 
# that the filesystem will be already large.
# If that does not happen for whatever reason, 200% seem 
# to be a safe enough bet and since it's a sparse file on disk
# it's not a download issue
IMAGE_OVERHEAD_FACTOR = "2"

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
