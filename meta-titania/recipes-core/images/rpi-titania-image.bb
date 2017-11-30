# Raspberry PI base image with splash and ssh
include recipes-core/images/rpi-basic-image.bb

# Monitoring backend
# TODO: migrate to python3 soon
IMAGE_INSTALL += "vuedj dapp-runner"

IMAGE_INSTALL += "docker networkmanager avahi-daemon llmnrd zram"

# Add firmware, this is needed for WiFi on RaspberryPi
IMAGE_INSTALL += "linux-firmware-bcm43430"

ROOTFS_POSTPROCESS_COMMAND += " titania_sysctl_config ; "

titania_sysctl_config() {
        # systemd sysctl config, add systemv if you want
        
        # Muting verbose printk() not to flood the console
        test -d ${IMAGE_ROOTFS}${sysconfdir}/sysctl.d && \
                echo "kernel.printk = 3 4 1 3" > ${IMAGE_ROOTFS}${sysconfdir}/sysctl.d/quiet-boot.conf
}



