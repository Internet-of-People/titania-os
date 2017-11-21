FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
SRC_URI += "file://admin.service"

do_install_append() {
    install -m 0644 ${WORKDIR}/admin.service ${D}${sysconfdir}/avahi/services/
}