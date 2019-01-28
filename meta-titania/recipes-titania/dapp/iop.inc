# See dapp.inc for explanation on why it's "," instead of "."
SYSTEMD_SERVICE_${PN} += "dapp@global,iop,ps.service     \
                          dapp@global,iop,can.service    \
                          dapp@global,iop,loc.service"

# Add IoP images to preinstall list
# TODO: somehow keep in sync with JSON?
# TODO: discuss desired behaviour here
DOCKER_IMAGE_PREINSTALL += "    \
    libertaria/iop-can:latest@sha256:9bf718e2835cbd4f2c459eee08b7b4587bd4b573668cf3c2bee92026e34738c1   \
    libertaria/iop-loc:latest@sha256:d8b14424b4cb045fb5cf69c1dcdaf9650c3346caa437bf3f094bcf193b16ec0a   \
    libertaria/iop-ps:latest@sha256:6b89a3cc3471c18a065862bb389a667e6a4a673e35691378287a8df31e8fbec0    \
    "
