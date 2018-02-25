# Add compressed root for SWupdate

# Re-initializing the types of the images
IMAGE_FSTYPES = "ext4 rpi-sdimg"
# Compressed version of the image
IMAGE_FSTYPES += "ext4.gz rpi-sdimg.gz"
# Informing RPi SDImg class what we've got
# TODO: decide if we should opt for a compressed one here?
SDIMG_ROOTFS_TYPE = "ext4"

# Cause datafs image to be built
do_image_rpi_sdimg[depends] += "titania-datafs-image:do_build"

# Raspberry PI base image with splash and ssh
include recipes-core/images/rpi-basic-image.bb

# Titania own software
IMAGE_INSTALL += "vuedj datafs-resizer"

IMAGE_INSTALL += "sudo networkmanager avahi-daemon llmnrd zram systemd-analyze swupdate"

# Docker
IMAGE_INSTALL += "docker docker-dapp docker-iop"

# TODO: replace with IPv6 or something eventually
IMAGE_INSTALL += "natpmp"

# Add firmware, this is needed for WiFi on RaspberryPi
IMAGE_INSTALL += "linux-firmware-bcm43430"

# Add custom groups
inherit extrausers
EXTRA_USERS_PARAMS += "groupadd wheel;"
# Disable passwordless root for non-debug builds
# TODO: is there a standard variable for this?
EXTRA_USERS_PARAMS += "usermod -L root;"

# Additinal systemctl variables
ROOTFS_POSTPROCESS_COMMAND += " titania_sysctl_config ; "

titania_sysctl_config() {
        # systemd sysctl config, add systemv if you want
        
        # Muting verbose printk() not to flood the console
        test -d ${IMAGE_ROOTFS}${sysconfdir}/sysctl.d && \
                echo "kernel.printk = 3 4 1 3" > ${IMAGE_ROOTFS}${sysconfdir}/sysctl.d/quiet-boot.conf
}

# Touch /var/lib/systemd/clock (location hardcoded in binary!) to the time of the build
# so that the clock is more reasonably initialized
ROOTFS_POSTPROCESS_COMMAND += " update_systemd_clock ; "

update_systemd_clock() {
    # TODO: WARNING: this seems to be /var/lib/systemd/timesync/clock in recent versions
    # update if the problem resurfaces
    touch ${IMAGE_ROOTFS}/var/lib/systemd/clock
}

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

IMAGE_CMD_rpi-sdimg_append() {
    # Modifying the name of the kernel on VFAT
    # TODO: is there a more elegant way?
    # TODO: `pyro` branch always names the kernel `uImage` whereas
    # `master` uses an env var. Watch out for upgrades.
    mdel -i ${WORKDIR}/boot.img ::${KERNEL_IMAGETYPE}
    mcopy -i ${WORKDIR}/boot.img -s ${DEPLOY_DIR_IMAGE}/${KERNEL_IMAGETYPE}${KERNEL_INITRAMFS}-${MACHINE}.bin ::${KERNEL_IMAGETYPE}_a

    # We need to rewrite the VFAT partition in order to avoid patching or copypasting meta-raspberrypi code
    dd if=${WORKDIR}/boot.img of=${SDIMG} conv=notrunc seek=1 bs=$(expr ${IMAGE_ROOTFS_ALIGNMENT} \* 1024)

    # Option: alternate between "uImage" and e.g. "uImage-alt"  but this is ugly and non-symmetrical naming

    # Update SD card image size
    # TODO: can we get IMAGE_SIZE from other image?
    DATAFS_SIZE=$(du --apparent-size -Hk "${DEPLOY_DIR_IMAGE}/${DATAFS_FILENAME}" | cut -f1)
    echo "Data file system is of ${DATAFS_SIZE} kiB in size"
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

    # Burning datafs
    # Using large `bs` for offsets results in serious memory requirements
    # TODO: maybe patch upstream
    dd if=${DEPLOY_DIR_IMAGE}/${DATAFS_FILENAME} of=${SDIMG} conv=notrunc seek=1024 bs=${DATAFS_START}

    parted ${SDIMG} print
}
