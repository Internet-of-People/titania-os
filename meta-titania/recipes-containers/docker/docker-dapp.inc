PACKAGES += "${PN}-dapp"
SYSTEMD_PACKAGES += "${PN}-dapp"

RDEPENDS_${PN}-dapp += "pydapphubfuse"

# TODO: move dapp_prepare.sh logic inside systemd
SRC_URI += "file://dapp@.service \
            file://dapp_prepare.sh"

# TODO: how exactly do we ship nginx?
# Drop-in directory for JSON maybe
FILES_${PN}-dapp = "${systemd_unitdir}/system/dapp@.service /opt/titania/*"

# TODO: doesn't work with templates
# TODO: solution temporarily included in docker-iop
SYSTEMD_SERVICE_${PN}-dapp = "dapp@nginx.service"

DOCKER_IMAGE_PREINSTALL += "libertaria/nginx:armv7"

do_install_append() {
    install -d ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/dapp@.service ${D}${systemd_unitdir}/system

    # TODO: variable for that
    install -d ${D}/opt/titania/bin
    install -m 0755 ${WORKDIR}/dapp_prepare.sh ${D}/opt/titania/bin
}
