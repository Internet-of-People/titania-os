# TODO: versioninig?
# TODO: RPi specific, maybe a MACHINE dependent switch?
SUMMARY = "systemd script to enlarge the filesystem on the SD card"
LICENSE = "GPL-3.0"

RDEPENDS_${PN} += "parted e2fsprogs-resize2fs systemd"

SRC_URI = "file://datafs-resizer.service \
           file://gplv3.md \
           file://datafs-resizer.sh \
           file://datafs.mount \
           file://var-lib-docker.mount"

LIC_FILES_CHKSUM = "file://${WORKDIR}/gplv3.md;md5=f149fa3bc39a974fe62c04649f34883a"

inherit systemd

FILES_${PN} = "${bindir}/datafs-resizer.sh \
               ${systemd_unitdir}/system/datafs-resizer.service \
               ${systemd_unitdir}/system/var-lib-docker.mount \
               ${systemd_unitdir}/system/datafs.mount \
               ${localstatedir}/lib/docker \
               /datafs"

SYSTEMD_SERVICE_${PN} = "datafs-resizer.service datafs.mount var-lib-docker.mount"

do_install() {
    # Mountpoints blanks
    install -d ${D}${localstatedir}/lib/docker
    install -d ${D}/datafs

    install -d ${D}${bindir}
    install -m 755 ${WORKDIR}/datafs-resizer.sh ${D}${bindir}

    install -d ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/datafs-resizer.service ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/var-lib-docker.mount ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/datafs.mount ${D}${systemd_unitdir}/system
}
