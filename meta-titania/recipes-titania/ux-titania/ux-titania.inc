# Using shortcuts before we all agree on naming
TITANIA_UX_BACKEND = "ux-titania"
TITANIA_UX_MONITOR = "monit-dashboard"

SRC_URI = "${LIBERTARIA_GIT_PREFIX}/titania-ux.git;protocol=${LIBERTARIA_GIT_PROTOCOL};branch=${UX_BRANCH} \
           file://${TITANIA_UX_BACKEND}.service \
           file://${TITANIA_UX_MONITOR}.service \
           file://start_${TITANIA_UX_BACKEND}.sh"
# TODO: override only for git versions, not in the base recipe
S = "${WORKDIR}/git"

# Pull Python in
# TODO: remove after we move to rust (dont forget to remove the layer too)
# TODO: we don't need sqlite in future
RDEPENDS_${PN} = "python3-django \
                  python3-pytz \
                  python3-misc \
                  python3-sqlite3 \
                  python3-djangorestframework \
                  python3-python-networkmanager \
                  sqlite3"

LICENSE = "GPL-3.0"
LIC_FILES_CHKSUM = "file://LICENCE.md;md5=8c40fdc41c95755623d451deddccda48"

inherit systemd

SYSTEMD_SERVICE_${PN} = "${TITANIA_UX_BACKEND}.service ${TITANIA_UX_MONITOR}.service"

# TODO: maybe find a more sophisticated place instead of /srv/?
FILES_${PN} += "/srv/ux-titania/ ${sysconfdir}/*"

do_install() {
    # cp is out of place here but works for now until we go Rust
    install -d ${D}/srv/ux-titania
    install -d ${D}/srv/ux-titania/dist
    cp -dr --no-preserve=ownership ${S}/vuedj/* ${D}/srv/ux-titania
    cp -dr --no-preserve=ownership ${S}/dist/* ${D}/srv/ux-titania/dist
    install -m 0755 ${WORKDIR}/start_${TITANIA_UX_BACKEND}.sh ${D}/srv/ux-titania/

    install -d ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/${TITANIA_UX_BACKEND}.service ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/${TITANIA_UX_MONITOR}.service ${D}${systemd_unitdir}/system

    # Track version
    install -d ${D}${sysconfdir}
    echo 'UX_ID="'${SRCREV}'"' > ${D}${sysconfdir}/titania-ux-version
}