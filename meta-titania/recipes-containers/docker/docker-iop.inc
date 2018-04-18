# Prepend to collect /etc before docker does
PACKAGES_prepend = "${PN}-iop "
SYSTEMD_PACKAGES += "${PN}-iop"

RDEPENDS_${PN}-dapp += "${PN}-dapp"

# TODO:Doesn't currently work with templates
SYSTEMD_SERVICE_${PN}-iop = "dapp@iopps.service     \
                             dapp@iopcan.service    \
                             dapp@ioploc.service"

# Add IoP images to preinstall list
DOCKER_IMAGE_PREINSTALL += "    \
    libertaria/iop-can:latest   \
    libertaria/iop-loc:latest   \
    libertaria/iop-ps:latest    \
    "

# TODO: replace with more robus implementation involving native systemd class means
DAPPS = "world.libertaria.nginx iop.global.iop.can iop.global.iop.ps iop.global.iop.loc"
FILES_${PN}-iop += "${sysconfdir}/system/multi-user.target.wants/dapp*"

do_install_append() {
    install -d ${D}${sysconfdir}/system/multi-user.target.wants/
    for dapp in ${DAPPS}; do
        ln -s /lib/systemd/system/dapp@.service ${D}${sysconfdir}/system/multi-user.target.wants/dapp@$dapp.service
    done
}