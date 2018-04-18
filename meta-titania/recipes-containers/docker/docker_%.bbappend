FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

# TODO: auto-start services are added to SYSTEMD_SERVICE-docker
# instead of respective packages. Study why do we have this limitation.
# The packages are unlikely to be installed w/o Docker anyway

require docker-fix-FILES.inc
require docker-preinstall.inc
require docker-dapp.inc
require docker-iop.inc
