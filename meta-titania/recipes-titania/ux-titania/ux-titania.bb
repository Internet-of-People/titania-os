inherit systemd

LICENSE = "GPL-3.0"
LIC_FILES_CHKSUM = "file://LICENCE.md;md5=8c40fdc41c95755623d451deddccda48"
SRC_URI = "file://ux.tar;subdir=ux-titania-1.0 \
           file://ux-titania.service \
           file://monit-dashboard.service \
           file://start_ux-titania.sh"

RDEPENDS_${PN} = "python3-django \
                  python3-pytz \
                  python3-misc \
                  python3-sqlite3 \
                  python3-djangorestframework \
                  python3-python-networkmanager \
                  sqlite3"

FILES_${PN} += "/srv/ux-titania/ ${sysconfdir}/*"

SYSTEMD_SERVICE_${PN} = "ux-titania.service monit-dashboard.service"


do_fetch_prepend() {
    import subprocess
    bb_dirname = os.path.dirname(d.getVar('BB_FILENAME'))
    subprocess.Popen(['tar', 'cvf', d.getVar('DL_DIR')+'/ux.tar', '-C', bb_dirname+'/../../../ux', '.']).wait()
}

do_install() {
    # cp is out of place here but works for now until we go Rust
    install -d ${D}/srv/ux-titania
    install -d ${D}/srv/ux-titania/dist
    cp -dr --no-preserve=ownership ${S}/vuedj/* ${D}/srv/ux-titania
    cp -dr --no-preserve=ownership ${S}/dist/* ${D}/srv/ux-titania/dist
    install -m 0755 ${WORKDIR}/start_ux-titania.sh ${D}/srv/ux-titania/

    install -d ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/ux-titania.service ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/monit-dashboard.service ${D}${systemd_unitdir}/system

    # Track version
    install -d ${D}${sysconfdir}
    echo 'UX_ID="'${SRCREV}'"' > ${D}${sysconfdir}/titania-ux-version
}
