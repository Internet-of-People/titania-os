# Re-initializing the types of the images, rpi-sdimg is not needed anymore
IMAGE_FSTYPES = "ext4 wic"

# Compressed version of the image (for SWupdate)
IMAGE_FSTYPES += " ext4.gz wic.gz"

# Informing RPi SDImg class what we've got
SDIMG_ROOTFS_TYPE = " ext4"

