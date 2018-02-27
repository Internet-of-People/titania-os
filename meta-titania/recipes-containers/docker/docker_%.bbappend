FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

# TODO: auto-start services are added to SYSTEMD_SERVICE-docker
# instead of respective packages. Study why do we have this limitation.
# The packages are unlikely to be installed w/o Docker anyway

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