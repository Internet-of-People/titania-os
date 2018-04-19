RDEPENDS_${PN} += "pydapphubfuse"

# TODO: move dapp_prepare.sh logic inside systemd
SRC_URI += "file://dapp@.service \
            file://dapp_prepare.sh"

# TODO: how exactly do we ship nginx?
# Drop-in directory for JSON maybe
FILES_${PN} = "${systemd_unitdir}/system/dapp@.service /opt/titania/*"

# SystemD recipe doesn't know how to parse things with multiple dots
# openembedded-core `master` branch has the correct code. 
# They get replaced in a ROOTFS_POSTPROCESS command (see rpi-titania-image)
# TODO: Either backport or upgrade branch (painful!), remove this hack
SYSTEMD_SERVICE_${PN} = "dapp@world,libertaria,nginx.service"

DOCKER_IMAGE_PREINSTALL += "libertaria/nginx:armv7"

do_install_append() {
    install -d ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/dapp@.service ${D}${systemd_unitdir}/system

    # TODO: variable for that
    install -d ${D}/opt/titania/bin
    install -m 0755 ${WORKDIR}/dapp_prepare.sh ${D}/opt/titania/bin
}
