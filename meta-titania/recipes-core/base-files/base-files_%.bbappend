FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
SRC_URI += "file://titania.ascii"

do_install_append() {
    # Add the Titania logo to /etc/issue
    cat ${D}${sysconfdir}/issue ${WORKDIR}/titania.ascii > ${D}${sysconfdir}/issue.titania
    mv ${D}${sysconfdir}/issue.titania ${D}${sysconfdir}/issue
}
