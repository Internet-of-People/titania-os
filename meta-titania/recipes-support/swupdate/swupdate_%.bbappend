FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
SRC_URI += "file://0001-unlink-UDS-after-use.patch \
            file://0002-http-style-progress.patch \
            file://after-everything.target \
            file://check-update.service \
            file://swupdate@.service \
            file://defconfig \
            file://check_update.sh \
            file://update_system.sh"

# We need u-boot-fw-utils on Titania, not just during the build
RDEPENDS_${PN} += "u-boot-fw-utils"
RDEPENDS_${PN} += "bash"

SYSTEMD_SERVICE_${PN} = "check-update.service after-everything.target"
FILES_${PN} += "${base_sbindir}/check_update.sh \
                ${base_sbindir}/update_system.sh \
                ${sysconfdir}/hwrevision \
                ${systemd_unitdir}/system/swupdate@.service"

do_install_append() {
    install -d ${D}${base_sbindir}
    install -m 0744 ${WORKDIR}/check_update.sh ${D}${base_sbindir}
    install -m 0744 ${WORKDIR}/update_system.sh ${D}${base_sbindir}
    install -m 0644 ${WORKDIR}/after-everything.target ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/check-update.service ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/swupdate@.service ${D}${systemd_unitdir}/system

    echo "${HWREVISION}" > ${D}${sysconfdir}/hwrevision

    # Make QA happy
    rm -f ${D}${systemd_unitdir}/system/swupdate.service
    rm -f ${D}${systemd_unitdir}/system/swupdate-*.service
    rm -fr ${D}${sysconfdir}/udev/
}
