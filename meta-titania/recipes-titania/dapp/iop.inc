# See dapp.inc for explanation on why it's "," instead of "."
SYSTEMD_SERVICE_${PN} += "dapp@global,iop,ps.service     \
                          dapp@global,iop,can.service    \
                          dapp@global,iop,loc.service"

# Add IoP images to preinstall list
# TODO: somehow keep in sync with JSON?
# TODO: discuss desired behaviour here
DOCKER_IMAGE_PREINSTALL += "    \
    libertaria/iop-can@sha256:97857277e0a9ec535560af8c31a5d1347c28d424fea94f5685abc7fc461dd086   \
    libertaria/iop-loc@sha256:7ea0b4f7e650a578cbc50e3a7032d131db76784fba878fdb2d29e324b3f3f2c6   \
    libertaria/iop-ps@sha256:8e098a552981a31f81dd175d7c2ee594ea41c8c54b5510e4ed695dfe894deec9    \
    "
