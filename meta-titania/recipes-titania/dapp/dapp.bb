FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
LICENSE = "GPL-3.0"
SRC_URI = "file://gplv3.md"
LIC_FILES_CHKSUM = "file://${WORKDIR}/gplv3.md;md5=f149fa3bc39a974fe62c04649f34883a"

inherit systemd

require dapp.inc
require iop.inc
require preinstall.inc
