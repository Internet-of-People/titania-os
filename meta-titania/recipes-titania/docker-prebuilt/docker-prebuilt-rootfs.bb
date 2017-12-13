SUMMARY = "Collection of images that are pre-installed on Docker"
SRC_URI += "file://nginx.service \
            file://iop-ps.service \
            file://iop-can.service \
            file://iop-loc.service \
            file://gplv3.md"

LICENSE = "GPL-3.0"
LIC_FILES_CHKSUM = "file://${WORKDIR}/gplv3.md;md5=f149fa3bc39a974fe62c04649f34883a"

inherit systemd

FILES_${PN} = "${systemd_unitdir}/system/nginx.service \
               ${systemd_unitdir}/system/iop-*.service"
               
SYSTEMD_SERVICE_${PN} = "nginx.service iop-ps.service iop-can.service iop-loc.service"

do_install_append() {
    # Install systemd units
    install -d ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/nginx.service ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/iop-*.service ${D}${systemd_unitdir}/system
}
