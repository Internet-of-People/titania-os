SUMMARY = "Collection of images that are pre-installed on Docker"
SRC_URI += "file://nginx.service \
            file://gplv3.md"

# or docker-native in future
DEPENDS_${PN} = "docker" 

LICENSE = "GPL-3.0"
LIC_FILES_CHKSUM = "file://${WORKDIR}/gplv3.md;md5=f149fa3bc39a974fe62c04649f34883a"

inherit systemd

do_install_append() {
    # Install systemd units
    install -d ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/nginx.service ${D}${systemd_unitdir}/system
}

INHIBIT_PACKAGE_STRIP = "1"
