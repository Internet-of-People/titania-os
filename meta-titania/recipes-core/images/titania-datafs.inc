# TODO: maybe separate in a dedicated include for more board support
# - issues: currently based directly on meta-raspberrypi

# Inject additional partitions:
# - Second root of size ROOTFS_SIZE
# - Data partition of DATAFS_SIZE (extended to the end of the drive on the first run)
# TODO: maybe split DATA partition to a separate state partition
# but this requires either GPT (bad for bootloader on RPi) or
# an extended partition
# TODO: label datafs?
# TOOD: can we query that somehow?
DATAFS_FILENAME ?= "titania-datafs-image-${MACHINE}.ext4"

# Cause datafs image to be built
##### do_image_rpi_sdimg[depends] += "titania-datafs-image:do_build"

^^^^ ez ki lett kommentelve, x86hoz


