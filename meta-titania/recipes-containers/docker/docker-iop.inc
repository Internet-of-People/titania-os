PACKAGES += "${PN}-iop"
SYSTEMD_PACKAGES += "${PN}-iop"

RDEPENDS_${PN}-dapp += "${PN}-dapp"

SYSTEMD_SERVICE_${PN}-iop = "dapp@iopps.service     \
                             dapp@iopcan.service    \
                             dapp@ioploc.service"

# Add IoP images to preinstall list
DOCKER_IMAGE_PREINSTALL += "    \
    libertaria/iop-can:latest   \
    libertaria/iop-loc:latest   \
    libertaria/iop-ps:latest    \
    "
