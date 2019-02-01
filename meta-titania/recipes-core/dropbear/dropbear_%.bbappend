FILESEXTRAPATHS_prepend := "${THISDIR}/dropbear:"

do_install_append() {
    rm ${D}${systemd_unitdir}/system/dropbearkey.service
    install -m 0644 ${WORKDIR}/systemd/dropbearkey@.service ${D}${systemd_unitdir}/system
    rm ${D}${systemd_unitdir}/system/dropbear@.service
    install -m 0644 ${WORKDIR}/systemd/dropbear@.service ${D}${systemd_unitdir}/system
    sed -i -e 's,@BASE_BINDIR@,${base_bindir},g' \
        -e 's,@BINDIR@,${bindir},g' \
        -e 's,@SBINDIR@,${sbindir},g' \
        ${D}${systemd_unitdir}/system/dropbear.socket ${D}${systemd_unitdir}/system/*.service
}

# make dropbear key handling compatible with openssh
EXTRA_OEMAKE += " NOSYSHOSTKEYLOAD=1 WRITEOPENSSHKEYS=1 OPENSSHHOSTKEYLOAD=1"

# Replacing the original dropbear with pts-dropbear URI
SRC_URI_remove = "http://matt.ucc.asn.au/dropbear/releases/dropbear-${PV}.tar.bz2"
SRC_URI += "git://github.com/pts/pts-dropbear;rev=7956b72e1b50088d27c70ea6e756c4b034d0cb31 \
            file://0010-disable-insecure-options.patch \
            file://systemd/dropbearkey@.service \
            file://systemd/dropbear@.service \
           "

SYSTEMD_SERVICE_${PN} += " dropbearkey@.service"

python do_unpack_append() {
    # pts-dropbear source can be found in 'pts-dropbear-2' directory instead of the canonical 'dropbear-2017.75'
    dropbear_dir = os.path.join(d.getVar('WORKDIR'), 'dropbear-' + d.getVar('PV'))
    os.rmdir(dropbear_dir)
    os.rename(os.path.join(d.getVar('WORKDIR'), 'git'), dropbear_dir)
}
