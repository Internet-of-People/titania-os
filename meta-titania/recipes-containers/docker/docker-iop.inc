PACKAGES += "${PN}-iop"

SRC_URI += "file://iop-ps.service   \
            file://iop-can.service  \
            file://iop-loc.service  \
            "

FILES_${PN}-iop = "${systemd_unitdir}/system/iop-*.service"

SYSTEMD_SERVICE_${PN}-iop = "iop-ps.service     \
                             iop-can.service    \
                             iop-loc.service"

# Add IoP images to preinstall list
DOCKER_IMAGE_PREINSTALL += "    \
    libertaria/iop-can:latest   \
    libertaria/iop-loc:latest   \
    libertaria/iop-ps:latest    \
    "

do_install_append() {
    install -d ${D}${systemd_unitdir}/system

    install -m 0644 ${WORKDIR}/iop-*.service ${D}${systemd_unitdir}/system
}
