# TODO: how to propagate updates? (i.e. bind reload with systemd)
SUMMARY = "Service to forward ports from containers on the router"
LICENSE = "GPL-3.0"

RDEPENDS_${PN} += "natpmp"

SRC_URI = "file://gplv3.md \
           file://forward-port@.service \
           file://forward_port.sh \
          "

LIC_FILES_CHKSUM = "file://${WORKDIR}/gplv3.md;md5=f149fa3bc39a974fe62c04649f34883a"

inherit systemd

FILES_${PN} += "/opt/titania ${systemd_unitdir}/system/"

do_install() {
    install -d ${D}/opt/titania/bin
    install -m 755 ${WORKDIR}/forward_port.sh ${D}/opt/titania/bin

    install -d ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/forward-port@.service ${D}${systemd_unitdir}/system
}