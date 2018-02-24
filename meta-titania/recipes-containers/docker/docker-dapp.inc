PACKAGES += "${PN}-dapp"

SRC_URI += "file://dapp@.service    \
            file://dapp-runner.sh   \ 
            file://nginx.service    \
            file://preinstall-docker-images.service \
            file://preinstall_docker_images.sh"

# TODO: does it make sense to ship nginx as part of this package or put it somewhere else rather?
FILES_${PN}-dapp = "${bindir}/dapp-runner.sh                                    \
                    ${bindir}/preinstall_docker_images.sh                       \
                    ${systemd_unitdir}/system/dapp@.service                     \
                    ${systemd_unitdir}/system/preinstall-docker-images.service  \
                    ${systemd_unitdir}/system/nginx.service"
SYSTEMD_SERVICE_${PN}-dapp = "nginx.service preinstall-docker-images.service"

DOCKER_IMAGE_PREINSTALL += "libertaria/nginx:armv7"

do_install_append() {
    install -d ${D}${systemd_unitdir}/system
    install -d ${D}${bindir}
    
    install -d ${D}${bindir}
    install -m 755 ${WORKDIR}/dapp-runner.sh ${D}${bindir}
    install -m 755 ${WORKDIR}/preinstall_docker_images.sh ${D}${bindir}

    install -m 0644 ${WORKDIR}/dapp@.service ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/preinstall-docker-images.service ${D}${systemd_unitdir}/system

    install -m 0644 ${WORKDIR}/nginx.service ${D}${systemd_unitdir}/system
}