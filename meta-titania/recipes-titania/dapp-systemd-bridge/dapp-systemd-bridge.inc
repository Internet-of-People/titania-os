SRC_URI = "${LIBERTARIA_GIT_PREFIX}/titania-dapps-systemd-bridge.git;protocol=${LIBERTARIA_GIT_PROTOCOL} \
           file://dapp-systemd-bridge.service \
           file://dapp-systemd-bridge-reload.service"
# TODO: override only for git versions, not in the base recipe
S = "${WORKDIR}/git"

# TODO: are we going to Rust?
RDEPENDS_${PN} = "python3-fusepy"

LICENSE = "GPL-3.0"
LIC_FILES_CHKSUM = "file://LICENSE.md;md5=f149fa3bc39a974fe62c04649f34883a"

inherit systemd

# TODO: make latter a .target, use ExecStartPost etc.
SYSTEMD_SERVICE_${PN} = "dapp-systemd-bridge.service dapp-systemd-bridge-reload.service"

# TODO: maybe find a more sophisticated place instead of /srv/?
FILES_${PN} += "/opt/titania/"

do_install() {
    # cp is out of place here but works for now until we go Rust
    install -d ${D}/opt/titania/bin
    install -d ${D}/opt/titania/share
    install -m 0755 ${S}/dapp-systemd-bridge.py ${D}/opt/titania/bin
    install -m 0644 ${S}/apps.json ${D}/opt/titania/share

    install -d ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/dapp-systemd-bridge.service ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/dapp-systemd-bridge-reload.service ${D}${systemd_unitdir}/system
}