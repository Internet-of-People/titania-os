FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
SRC_URI += "file://0001-unlink-UDS-after-use.patch \
            file://0002-http-style-progress.patch \
            file://after-everything.target \
            file://check-update.service \
            file://swupdate@.service \
            file://defconfig \
            file://check_update.sh \
            file://update_system.sh"

# TODO: we probably don't care but ideally we should honor the config file 
# and check if CONFIG_UBOOT is set
# see swupdate.inc for template

# We need u-boot-fw-utils on Titania, not just during the build
RDEPENDS_${PN} += "u-boot-fw-utils"

# TODO: add progress indicator service
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

    # TODO: generalize based on MACHINE info
    echo "raspberrypi 3" > ${D}${sysconfdir}/hwrevision

    # Make QA happy
    rm -f ${D}${systemd_unitdir}/system/swupdate.service
    rm -f ${D}${systemd_unitdir}/system/swupdate-*.service
    rm -fr ${D}${sysconfdir}/udev/
}