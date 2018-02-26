FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

require docker-fix-FILES.inc
require docker-preinstall.inc
require docker-dapp.inc
# TODO: remove docker-iop after generalisation with docker-dapp
require docker-iop.inc

FILES_${PN} += "${localstatedir/lib/docker"

do_install_append() {
    # Empty anchor for binding mount
    # TODO: ownership and permissions?
    install -d ${D}${localstatedir}/lib/docker
}