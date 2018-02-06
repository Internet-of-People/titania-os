FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
SRC_URI += "file://titania.ascii \
            file://fstab \
            file://0001-sbin-for-not-root-user.patch;patchdir=${WORKDIR}"

hostname = "titania"

do_install_append() {
    # Add the Titania logo to /etc/issue
    cat ${WORKDIR}/titania.ascii ${D}${sysconfdir}/issue > ${WORKDIR}/issue.titania
    install -m 0644 ${WORKDIR}/issue.titania ${D}${sysconfdir}/issue
    install -m 0644 ${WORKDIR}/titania.ascii ${D}${sysconfdir}/issue.net
}
