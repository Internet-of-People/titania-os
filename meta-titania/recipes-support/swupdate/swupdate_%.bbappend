FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
SRC_URI += "file://after-everything.target \
            file://update-check.service \
            file://update_check.sh"

# TODO: we probably don't care but ideally we should honor the config file 
# and check if CONFIG_UBOOT is set
# see swupdate.inc for template

# We need u-boot-fw-utils on Titania, not just during the build
RDEPENDS_${PN} += "u-boot-fw-utils"

SYSTEMD_SERVICE_${PN} += "update-check.service after-everything.target"
FILES_${PN} += "${base_sbindir}/update_check.sh"

do_install_append() {
    install -d ${D}${base_sbindir}
    install -m 0744 ${WORKDIR}/update_check.sh ${D}${base_sbindir}
    install -m 0644 ${WORKDIR}/after-everything.target ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/update-check.service ${D}${systemd_unitdir}/system
}