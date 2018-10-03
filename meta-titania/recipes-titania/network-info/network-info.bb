# TODO: when to restart/update? 
# TODO: how to propagate updates? (i.e. bind reload with systemd)
SUMMARY = "Service to collect basic geolocation and ip information"
LICENSE = "GPL-3.0"

# TODO: TYO-19, change to whatever ssl library we end up using
RDEPENDS_${PN} += "natpmp dropbear openssl curl"

SRC_URI = "file://gplv3.md \
           file://network-info.service \
           file://network_info.sh \
          "

LIC_FILES_CHKSUM = "file://${WORKDIR}/gplv3.md;md5=f149fa3bc39a974fe62c04649f34883a"

inherit systemd

FILES_${PN} += "/opt/titania ${systemd_unitdir}/system/"

SYSTEMD_SERVICE_${PN} = "network-info.service"

do_install() {
    install -d ${D}/opt/titania/bin
    install -m 755 ${WORKDIR}/network_info.sh ${D}/opt/titania/bin

    install -d ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/network-info.service ${D}${systemd_unitdir}/system
}