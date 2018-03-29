# TODO: replace with HTTPS link when we go public
SRC_URI = "git://git@gitlab.libertaria.community:2200/titania/pydapphubfuse.git;protocol=ssh \
           file://pydapphubfuse.service"
# TODO: override only for git versions, not in the base recipe
S = "${WORKDIR}/git"

# TODO: are we going to Rust?
RDEPENDS_${PN} = "python3-fusepy"

LICENSE = "GPL-3.0"
LIC_FILES_CHKSUM = "file://LICENSE;md5=e11ab5963417f9fd40fe04c3cf8c6f74"

inherit systemd

SYSTEMD_SERVICE_${PN} = "pydapphubfuse.service"

# TODO: maybe find a more sophisticated place instead of /srv/?
FILES_${PN} += "/srv/pydapphubfuse/"

do_install() {
    # cp is out of place here but works for now until we go Rust
    install -d ${D}/srv/pydapphubfuse
    install -m 0755 ${S}/pydapphubfuse.py ${D}/srv/pydapphubfuse/
    install -m 0644 ${S}/apps.json ${D}/srv/pydapphubfuse/

    install -d ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/pydapphubfuse.service ${D}${systemd_unitdir}/system
}