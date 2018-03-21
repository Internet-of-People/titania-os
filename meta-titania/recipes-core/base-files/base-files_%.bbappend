FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
SRC_URI += "file://titania.ascii \
            file://fstab \
            file://0001-sbin-for-not-root-user.patch;patchdir=${WORKDIR}"

hostname = "titania"

FILES_${PN} += "/datafs"

# TODO: apply same logic to other packages with package-split collection order issues
PACKAGES_prepend = "${PN}-datafs "
FILES_${PN}-datafs = "/titania/home /titania/config"

do_install_append() {
    # Add the Titania logo to /etc/issue
    cat ${WORKDIR}/titania.ascii ${D}${sysconfdir}/issue > ${WORKDIR}/issue.titania
    install -m 0644 ${WORKDIR}/issue.titania ${D}${sysconfdir}/issue
    install -m 0644 ${WORKDIR}/titania.ascii ${D}${sysconfdir}/issue.net

    # DataFS
    install -d ${D}/titania
    mv ${D}/home ${D}/titania/home
    install -d ${D}/titania/config

    # Mountpoint blanks
    # TODO: verify if it's safe to remove
    install -d ${D}/datafs
    install -d ${D}/home
}
