FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
SRC_URI += "file://0001-systemd-reuse-sysv-service.patch;patchdir=../"

FILES_${PN} += "${bindir}/zram"

do_install_append() {
    # Rename the SysV script
    install -d ${D}${bindir}
    mv ${D}${sysconfdir}/init.d/zram ${D}${bindir}/zram
}
