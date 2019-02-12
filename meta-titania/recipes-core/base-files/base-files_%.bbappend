FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
SRC_URI += "file://titania.ascii \
            file://fstab \
            file://0001-sbin-for-not-root-user.patch;patchdir=${WORKDIR} \
            file://mirror.sh \
            file://mirror@.service"

hostname = "titania"

FILES_${PN} += "/datafs"

# TODO: apply same logic to other packages with package-split collection order issues
PACKAGES_prepend = "${PN}-datafs "
FILES_${PN}-datafs = "/titania/home /titania/config"

do_install_append() {
    mv ${D}${sysconfdir}/issue ${D}${sysconfdir}/issue.titania
    # Add the Titania logo to /etc/titania.ascii
    install -m 0644 ${WORKDIR}/titania.ascii ${D}${sysconfdir}/

    # DataFS
    install -d ${D}/titania
    mv ${D}/home ${D}/titania/home
    install -d ${D}/titania/config

    # Mountpoint blanks
    install -d ${D}/datafs
    install -d ${D}/home

    # TODO: this doesn't belong to this package! Please move
    install -d ${D}${bindir}
    install -d ${D}/lib/systemd/system
    install -m 0644 ${WORKDIR}/mirror@.service ${D}/lib/systemd/system
    install -m 0755 ${WORKDIR}/mirror.sh ${D}${bindir}
}
