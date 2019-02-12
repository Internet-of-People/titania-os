SUMMARY = "systemd script to enlarge the filesystem on the storage"
LICENSE = "GPL-3.0"

RDEPENDS_${PN} += "parted e2fsprogs-resize2fs systemd bash"

SRC_URI = "file://gplv3.md \
           file://titania-grow-datafs.service \
           file://titania-grow-datafs.sh \
          "

LIC_FILES_CHKSUM = "file://${WORKDIR}/gplv3.md;md5=f149fa3bc39a974fe62c04649f34883a"

inherit systemd

FILES_${PN} = "/opt/titania/bin/titania-grow-datafs.sh \
               ${systemd_unitdir}/system/titania-grow-datafs.service \
              "

SYSTEMD_SERVICE_${PN} = "titania-grow-datafs.service"

do_install() {
    install -d ${D}/opt/titania/bin
    install -m 755 ${WORKDIR}/titania-grow-datafs.sh ${D}/opt/titania/bin

    install -d ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/titania-grow-datafs.service ${D}${systemd_unitdir}/system
}
