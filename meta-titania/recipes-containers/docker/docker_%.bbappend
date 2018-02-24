FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

require docker-fix-FILES.inc
require docker-preinstall.inc
require docker-dapp.inc
# TODO: remove docker-iop after generalisation with docker-dapp
require docker-iop.inc


