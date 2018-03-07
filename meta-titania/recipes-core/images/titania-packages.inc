# Titania own software
IMAGE_INSTALL += "vuedj datafs-resizer http-splash"

IMAGE_INSTALL += "sudo networkmanager avahi-daemon llmnrd zram systemd-analyze swupdate"

# Docker
IMAGE_INSTALL += "docker docker-dapp docker-iop"

# TODO: replace with IPv6 or something eventually
IMAGE_INSTALL += "natpmp"

# Add firmware, this is needed for WiFi on RaspberryPi
IMAGE_INSTALL += "linux-firmware-bcm43430"