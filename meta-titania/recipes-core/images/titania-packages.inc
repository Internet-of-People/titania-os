# Titania own software
IMAGE_INSTALL += "ux-titania datafs-resizer http-splash"

IMAGE_INSTALL += "sudo zram systemd-analyze"

# Network and discovery
IMAGE_INSTALL += "networkmanager avahi-daemon llmnrd"

# SWupdate
IMAGE_INSTALL += "swupdate"

# Docker
IMAGE_INSTALL += "docker docker-dapp"

# TODO: replace with IPv6 or something eventually
IMAGE_INSTALL += "natpmp"

# Add firmware, this is needed for WiFi on RaspberryPi
IMAGE_INSTALL += "linux-firmware-bcm43430"

# Merge UX version with main OS-release file
append_ux_id () {
    cat ${IMAGE_ROOTFS}${sysconfdir}/titania-ux-version >> ${IMAGE_ROOTFS}${sysconfdir}/os-release
    rm ${IMAGE_ROOTFS}${sysconfdir}/titania-ux-version
}
ROOTFS_POSTPROCESS_COMMAND += "append_ux_id ; "
