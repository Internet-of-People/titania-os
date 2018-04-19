# TODO: replace with HTTPS link when we go public
SRC_URI = "git://git@gitlab.libertaria.community:2200/titania/pydapphubfuse.git;protocol=ssh \
           file://pydapphubfuse.service \
           file://pydapphubfuse-reload.service"
# TODO: override only for git versions, not in the base recipe
S = "${WORKDIR}/git"

# TODO: are we going to Rust?
RDEPENDS_${PN} = "python3-fusepy"

LICENSE = "GPL-3.0"
LIC_FILES_CHKSUM = "file://LICENSE;md5=e11ab5963417f9fd40fe04c3cf8c6f74"

inherit systemd

# TODO: make latter a .target, use ExecStartPost etc.
SYSTEMD_SERVICE_${PN} = "pydapphubfuse.service pydapphubfuse-reload.service"

# TODO: maybe find a more sophisticated place instead of /srv/?
FILES_${PN} += "/opt/titania/"

do_install() {
    # cp is out of place here but works for now until we go Rust
    install -d ${D}/opt/titania/bin
    install -d ${D}/opt/titania/share
    install -m 0755 ${S}/pydapphubfuse.py ${D}/opt/titania/bin
    install -m 0644 ${S}/apps.json ${D}/opt/titania/share

    install -d ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/pydapphubfuse.service ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/pydapphubfuse-reload.service ${D}${systemd_unitdir}/system
}