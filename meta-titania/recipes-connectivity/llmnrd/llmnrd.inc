SUMMARY = "Link-Local Multicast Resolution (LLMNR) Daemon for Linux"
LICENSE = "GPL-2.0"
LIC_FILES_CHKSUM = "file://COPYING;md5=05a4c5604b9126dcb84dcc6f1a84a7bb"
HOMEPAGE = "https://github.com/tklauser/llmnrd"

# TODO: check ASC signatures
SRC_URI = "https://github.com/tklauser/llmnrd/releases/download/v${PV}/llmnrd-${PV}.tar.bz2"
SRC_URI[md5sum] = "48e56b3ded18c8d385333dcc82dbb9f2"
SRC_URI[sha256sum] = "6fd499affb80acfa089704df6d6579138b853270e177d57dc6f3d2e9faf3cae7"

inherit systemd

SYSTEMD_SERVICE_${PN} = "llmnrd.service"

EXTRA_OEMAKE = "prefix=${prefix} DESTDIR=${D} CROSS_COMPILE=${TARGET_PREFIX} 'CC=${CC}' 'LD=${LD}'"

do_install() {
    oe_runmake install 

    install -d ${D}${systemd_unitdir}/system
    install -m 0644 ${S}/etc/llmnrd.service ${D}${systemd_unitdir}/system
}
