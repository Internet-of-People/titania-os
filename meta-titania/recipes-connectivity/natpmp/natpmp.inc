SUMMARY = "NAT-PMP protocpl client and few goodies"

# TODO split into packages

LICENSE = "BSD"
LIC_FILES_CHKSUM = "file://LICENSE;md5=63b8bf0fd09f4909d823a94c6e6fc06b"
HOMEPAGE = "http://miniupnp.free.fr/"

SRC_URI = "http://miniupnp.free.fr/files/download.php?file=libnatpmp-${PV}.tar.gz\
          file://forward-port@.service \
          file://forward_port.sh \
          file://network_info.sh \
          file://network-info.service"
          
SRC_URI[md5sum] = "7bd1af6710271e1743df5422be350bd8"
SRC_URI[sha256sum] = "e1aa9c4c4219bc06943d6b2130f664daee213fb262fcb94dd355815b8f4536b0"

inherit systemd

EXTRA_OEMAKE = "CROSS_COMPILE=${TARGET_PREFIX} 'CC=${CC}' 'LD=${LD}'"

# Fix source directory
S = "${WORKDIR}/lib${PN}-${PV}/"

FILES_${PN} += "${systemd_unitdir}/system/forward-port@.service ${bindir}/network_info.sh ${bindir}/forward_port.sh ${systemd_unitdir}/system/network-info.service"

SYSTEMD_SERVICE_${PN} = "network-info.service"

do_install() {
    # Manually install what we need
    # TODO: maybe /sbin for network info?
    # TODO: maybe network-info service instead of underscore?
    install -d ${D}${bindir}
    install -m 0755 ${S}/natpmpc-static ${D}${bindir}/natpmpc
    install -m 0755 ${WORKDIR}/network_info.sh ${D}${bindir}
    install -m 0755 ${WORKDIR}/forward_port.sh ${D}${bindir}
    install -d ${D}${mandir}
    install -m 0644 ${S}/natpmpc.1 ${D}${mandir}

    install -d ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/forward-port@.service ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/network-info.service ${D}${systemd_unitdir}/system
}
