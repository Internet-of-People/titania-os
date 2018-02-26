# TODO: versioninig?
# TODO: RPi specific, maybe a MACHINE dependent switch?
SUMMARY = "systemd script to enlarge the filesystem on the SD card"
LICENSE = "GPL-3.0"

RDEPENDS_${PN} += "parted e2fsprogs-resize2fs systemd"

SRC_URI = "file://gplv3.md \
           file://datafs-growfs.service \
           file://datafs-grow-partition.service \
           file://datafs-grow-partition.sh \
          "

LIC_FILES_CHKSUM = "file://${WORKDIR}/gplv3.md;md5=f149fa3bc39a974fe62c04649f34883a"

inherit systemd

FILES_${PN} = "${bindir}/datafs-grow-partition.sh \
               ${systemd_unitdir}/system/datafs-grow-partition.service \
               ${systemd_unitdir}/system/datafs-growfs.service \
              "

SYSTEMD_SERVICE_${PN} = "datafs-grow-partition.service datafs-growfs.service"

do_install() {
    install -d ${D}${bindir}
    install -m 755 ${WORKDIR}/datafs-grow-partition.sh ${D}${bindir}

    install -d ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/datafs-grow-partition.service ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/datafs-growfs.service ${D}${systemd_unitdir}/system
}
