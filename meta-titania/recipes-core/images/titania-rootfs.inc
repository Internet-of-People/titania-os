# Add compressed root for SWupdate

# Re-initializing the types of the images
IMAGE_FSTYPES = "ext4 rpi-sdimg"
# Compressed version of the image
IMAGE_FSTYPES += "ext4.gz rpi-sdimg.gz"
# Informing RPi SDImg class what we've got
# TODO: decide if we should opt for a compressed one here?
SDIMG_ROOTFS_TYPE = "ext4"

# Force 500 MiB partition
ROOTFS_SIZE_LIMIT = "512000"

# TODO: this is naïve calculation based on image.bbclass, might not be portable
IMAGE_ROOTFS_MAXSIZE = "516096"
IMAGE_ROOTFS_SIZE = "${ROOTFS_SIZE_LIMIT}"

# NOTE: this gets auto-corrected slightly because of alignment calculation
# in image.bbclass, but still results in a predictable partition size