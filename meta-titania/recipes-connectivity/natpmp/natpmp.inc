SUMMARY = "NAT-PMP protocpl client and few goodies"
LICENSE = "BSD"
LIC_FILES_CHKSUM = "file://LICENSE;md5=63b8bf0fd09f4909d823a94c6e6fc06b"
HOMEPAGE = "http://miniupnp.free.fr/"

SRC_URI = "http://miniupnp.free.fr/files/download.php?file=libnatpmp-${PV}.tar.gz\
          file://forward_port@.service \
          file://network_info.sh \
          file://network_info.service"
          
SRC_URI[md5sum] = "7bd1af6710271e1743df5422be350bd8"
SRC_URI[sha256sum] = "e1aa9c4c4219bc06943d6b2130f664daee213fb262fcb94dd355815b8f4536b0"

inherit systemd

EXTRA_OEMAKE = "CROSS_COMPILE=${TARGET_PREFIX} 'CC=${CC}' 'LD=${LD}'"

# Fix source directory
S = "${WORKDIR}/lib${PN}-${PV}/"

FILES_${PN} += "${systemd_unitdir}/system/forward_port@.service ${bindir}/network_info.sh ${systemd_unitdir}/system/network_info.service"

SYSTEMD_SERVICE_${PN} = "network_info.service"

do_install() {
    # Manually install what we need
    install -d ${D}${bindir}
    install -m 0755 ${S}/natpmpc-static ${D}${bindir}/natpmpc
    install -m 0755 ${WORKDIR}/network_info.sh ${D}${bindir}/network_info.sh
    install -d ${D}${mandir}
    install -m 0644 ${S}/natpmpc.1 ${D}${mandir}

    install -d ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/forward_port@.service ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/network_info.service ${D}${systemd_unitdir}/system
}
