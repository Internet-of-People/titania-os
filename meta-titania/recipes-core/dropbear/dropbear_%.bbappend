# Set the welcome banner to /etc/issue.net
do_install_append() {
    echo "DROPBEAR_EXTRA_ARGS=\"-b ${sysconfdir}/issue.net\"" > ${D}${sysconfdir}/default/dropbear
}

# make dropbear key handling compatible with openssh
EXTRA_OEMAKE += " NOSYSHOSTKEYLOAD=1 WRITEOPENSSHKEYS=1 OPENSSHHOSTKEYLOAD=1"

SRC_URI = "git://github.com/pts/pts-dropbear;rev=a9f901e76377ba3c6dcb7254e5467a813c1e28ef \
           file://0001-urandom-xauth-changes-to-options.h.patch \
           file://0003-configure.patch \
           file://0004-fix-2kb-keys.patch \
           file://0007-dropbear-fix-for-x32-abi.patch \
           file://0010-disable-insecure-options.patch \
           file://fix-libtomcrypt-libtommath-ordering.patch \
           file://init \
           file://dropbearkey.service \
           file://dropbear@.service \
           file://dropbear.socket \
           ${@bb.utils.contains('DISTRO_FEATURES', 'pam', '${PAM_SRC_URI}', '', d)} "

python do_unpack_append() {
    # pts-dropbear source can be found in 'pts-dropbear-2' directory instead of the canonical 'dropbear-2017.75'
    dropbear_dir = os.path.join(d.getVar('WORKDIR'), 'dropbear-' + d.getVar('PV'))
    os.rmdir(dropbear_dir)
    os.rename(os.path.join(d.getVar('WORKDIR'), 'git'), dropbear_dir)
}
