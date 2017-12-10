# Raspberry PI base image with splash and ssh
include recipes-core/images/rpi-basic-image.bb

# We need the data filesystem
DEPENDS += "docker-prebuilt-datafs"

# Monitoring backend
# TODO: migrate to python3 soon
IMAGE_INSTALL += "vuedj dapp-runner docker-prebuilt-rootfs datafs-resizer"

IMAGE_INSTALL += "sudo docker networkmanager avahi-daemon llmnrd zram systemd-analyze"

# TODO: replace with IPv6 or something eventually
IMAGE_INSTALL += "natpmp"

# TODO: we won't need this in future
IMAGE_INSTALL += "sqlite3"

# Add firmware, this is needed for WiFi on RaspberryPi
IMAGE_INSTALL += "linux-firmware-bcm43430"

# Add custom groups
inherit extrausers
EXTRA_USERS_PARAMS += "groupadd wheel;"
# Disable passwordless root for non-debug builds
# TODO: is there a standard variable for this?
EXTRA_USERS_PARAMS += "${@ 'usermod -L root;' if not d.getVar('TITANIA_DEBUG') else ''}"

ROOTFS_POSTPROCESS_COMMAND += " titania_sysctl_config ; "

titania_sysctl_config() {
        # systemd sysctl config, add systemv if you want
        
        # Muting verbose printk() not to flood the console
        test -d ${IMAGE_ROOTFS}${sysconfdir}/sysctl.d && \
                echo "kernel.printk = 3 4 1 3" > ${IMAGE_ROOTFS}${sysconfdir}/sysctl.d/quiet-boot.conf
}

# TODO: maybe separate in a dedicated include for more board support
# - issues: currently based directly on meta-raspberrypi

# Inject additional partitions:
# - Second root of size ROOTFS_SIZE
# - Data partition of DATAFS_SIZE (extended to the end of the drive on the first run)
# TODO: maybe split DATA partition to a separate state partition
# but this requires either GPT (bad for bootloader on RPi) or
# an extended partition
DATAFS_SIZE ?= "245760"
DATAFS_LABEL ?= "data"

IMAGE_CMD_rpi-sdimg_append() {
    # Update SD card image size
    NEW_SDIMG_SIZE=$(expr ${SDIMG_SIZE} + ${ROOTFS_SIZE} + ${DATAFS_SIZE})
    dd if=/dev/zero of=${SDIMG} bs=1024 count=0 seek=${NEW_SDIMG_SIZE}

    # Start locations of second root and data
    # TODO: check alignment
    # TODO: special meaning to -1s in meta-raspberrypi?
    ROOT_B_START=${SDIMG_SIZE}
    ROOT_B_END=$(expr ${ROOTFS_SIZE} + ${SDIMG_SIZE})
    DATAFS_START=${ROOT_B_END}
    DATAFS_END=$(expr ${NEW_SDIMG_SIZE} - 1)

    # Create additional partitions
    parted -s ${SDIMG} unit KiB mkpart primary ext2 ${ROOT_B_START} ${ROOT_B_END}
    parted -s ${SDIMG} unit KiB mkpart primary ext2 ${DATAFS_START} ${DATAFS_END}

    # We currently leave RootB empty to preserve space of the image
    # This is where the flasher would be putting the update anyway

    # Generate the data partition
    # TODO: tune ext4fs params
    rm -f ${WORKDIR}/data.img
    DATAFS_BLOCKS=$(LC_ALL=C parted -s ${SDIMG} unit b print | awk '/ 4 / { print substr($4, 1, length($4 -1)) / 512 /2 }')

    # NOTE TODO: RPi-dependent, find a general way
    DATA_ROOT=${WORKDIR}/../../../cortexa7hf-neon-vfpv4-oe-linux-gnueabi/docker-prebuilt-datafs/1.0-r0/image
    mkfs.ext4 ${WORKDIR}/data.img $DATAFS_BLOCKS -L ${DATAFS_LABEL} -d $DATA_ROOT
    dd if=${WORKDIR}/data.img of=${SDIMG} conv=notrunc seek=1 bs=$(expr 1024 \* ${DATAFS_START})

    parted ${SDIMG} print
}
