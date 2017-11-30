# TODO: versioninig?
SUMMARY = "systemd helper scripts to run Docker containers"
LICENSE = "GPL-3.0"

SRC_URI = "file://dapp@.service \
           file://gplv3.md \
           file://dapp-runner.sh"

LIC_FILES_CHKSUM = "file://${WORKDIR}/gplv3.md;md5=f149fa3bc39a974fe62c04649f34883a"

inherit systemd

RDEPENDS_${PN} = "docker systemd"

FILES_${PN} = "${bindir}/dapp-runner.sh ${systemd_unitdir}/system/dapp@.service"

do_install() {
    install -d ${D}${bindir}
    install -m 755 ${WORKDIR}/dapp-runner.sh ${D}${bindir}

    install -d ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/dapp@.service ${D}${systemd_unitdir}/system
}
