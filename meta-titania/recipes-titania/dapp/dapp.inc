RDEPENDS_${PN} += "pydapphubfuse"

# TODO: move dapp_prepare.sh logic inside systemd
SRC_URI += "file://dapp@.service \
            file://dapp_prepare.sh \
            file://dapp_register.sh \
            file://dapp_pull.sh \
            file://dapp_load.sh \
            file://dapp_version.sh \
            file://nginx-reload-support.conf \
            file://nginx-custom-paths.conf"

# TODO: how exactly do we ship nginx?
# Drop-in directory for JSON maybe
FILES_${PN} = "${systemd_unitdir}/system/dapp@.service /opt/titania/* ${sysconfdir}/systemd/*"

# SystemD recipe doesn't know how to parse things with multiple dots
# openembedded-core `master` branch has the correct code. 
# They get replaced in a ROOTFS_POSTPROCESS command (see rpi-titania-image)
# TODO: Either backport or upgrade branch (painful!), remove this hack
SYSTEMD_SERVICE_${PN} = "dapp@world,libertaria,nginx.service"

NGINX_SERVICE="dapp@world.libertaria.nginx"

# TODO: this is dapp_test tag, merge everything and streamline!
DOCKER_IMAGE_PREINSTALL += "libertaria/nginx:armv7@sha256:b1f0883cc1e7ed829bb053b46339545bd6dbddc202d00cef0478642eb4e36850"

do_install_append() {
    install -d ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/dapp@.service ${D}${systemd_unitdir}/system

    install -d ${D}${sysconfdir}/systemd/system/${NGINX_SERVICE}.service.d
    install -m 0644 ${WORKDIR}/nginx-reload-support.conf ${D}${sysconfdir}/systemd/system/${NGINX_SERVICE}.service.d
    install -m 0644 ${WORKDIR}/nginx-custom-paths.conf ${D}${sysconfdir}/systemd/system/${NGINX_SERVICE}.service.d

    # TODO: variable for that
    install -d ${D}/opt/titania/bin
    install -m 0755 ${WORKDIR}/dapp_*.sh ${D}/opt/titania/bin
}
