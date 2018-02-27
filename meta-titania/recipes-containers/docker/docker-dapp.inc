PACKAGES += "${PN}-dapp"
SYSTEMD_PACKAGES += "${PN}-dapp"

SRC_URI += "file://dapp@.service    \
            file://dapp-runner.sh   \ 
            file://nginx.service    \
            file://image-preinstall@.service \
            file://image_preinstall.sh"

# TODO: does it make sense to ship nginx as part of this package or put it somewhere else rather?
FILES_${PN}-dapp = "${bindir}/dapp-runner.sh                                    \
                    ${bindir}/image_preinstall.sh                               \
                    ${systemd_unitdir}/system/dapp@.service                     \
                    ${systemd_unitdir}/system/image-preinstall@.service         \
                    ${systemd_unitdir}/system/nginx.service"
SYSTEMD_SERVICE_${PN}-dapp = "nginx.service"

DOCKER_IMAGE_PREINSTALL += "libertaria/nginx:armv7"

do_install_append() {
    install -d ${D}${systemd_unitdir}/system
    install -d ${D}${bindir}
    
    install -d ${D}${bindir}
    install -m 755 ${WORKDIR}/dapp-runner.sh ${D}${bindir}
    install -m 755 ${WORKDIR}/image_preinstall.sh ${D}${bindir}

    install -m 0644 ${WORKDIR}/dapp@.service ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/image-preinstall@.service ${D}${systemd_unitdir}/system

    install -m 0644 ${WORKDIR}/nginx.service ${D}${systemd_unitdir}/system
}