# See dapp.inc for explanation on why it's "," instead of "."
SYSTEMD_SERVICE_${PN} += "dapp@iop,global,iop,ps.service     \
                          dapp@iop,global,iop,can.service    \
                          dapp@iop,global,iop,loc.service"

# Add IoP images to preinstall list
DOCKER_IMAGE_PREINSTALL += "    \
    libertaria/iop-can:latest   \
    libertaria/iop-loc:latest   \
    libertaria/iop-ps:latest    \
    "
