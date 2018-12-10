RDEPENDS_${PN} = " \
    bash \
    inotify-tools \
    python3-fusepy \
    python3-modules \
    python3-misc \
"

# TODO: move dapp_prepare.sh logic inside systemd
SRC_URI += "file://apps.json \
            file://dapp_prepare.sh \
            file://dapp_register.sh \
            file://dapp_pull.sh \
            file://dapp_load.sh \
            file://dapp_version.sh \
            file://dapp_update.sh \
            file://dapp_json_merge.py \
            file://dapp_systemd_bridge.py \
            file://systemd/dapp@.service \
            file://systemd/nginx-reload-support.conf \
            file://systemd/nginx-custom-paths.conf \
            file://systemd/dapp-systemd-bridge.service \
            file://systemd/dapp-json-merge.service"

inherit systemd

# TODO: how exactly do we ship nginx?
# Drop-in directory for JSON maybe
FILES_${PN} = "${systemd_unitdir}/system/dapp@.service /opt/titania/* ${sysconfdir}/systemd/* /opt/titania/"

# Systemd recipe doesn't know how to parse things with multiple dots
# openembedded-core `master` branch has the correct code. 
# They get replaced in a ROOTFS_POSTPROCESS command (see rpi-titania-image)
# TODO: Either backport or upgrade branch (painful!), remove this hack
# TODO: make latter a .target, use ExecStartPost etc.
SYSTEMD_SERVICE_${PN} = "dapp@world,libertaria,nginx.service \
                         dapp-systemd-bridge.service \
                         dapp-json-merge.service"

NGINX_SERVICE="dapp@world.libertaria.nginx"

DOCKER_IMAGE_PREINSTALL += "libertaria/nginx:latest@sha256:93295c18e9876c412deb3ef09bdffdf7c7d8367e9c069e05c7d90a8d0f44907f"

do_install_append() {
    install -d ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/systemd/dapp@.service ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/systemd/dapp-systemd-bridge.service ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/systemd/dapp-json-merge.service ${D}${systemd_unitdir}/system

    install -d ${D}${sysconfdir}/systemd/system/${NGINX_SERVICE}.service.d
    install -m 0644 ${WORKDIR}/systemd/nginx-*.conf ${D}${sysconfdir}/systemd/system/${NGINX_SERVICE}.service.d
    
    install -d ${D}/opt/titania/bin
    install -d ${D}/opt/titania/share

    install -m 0755 ${WORKDIR}/dapp_*.sh ${D}/opt/titania/bin
    install -m 0755 ${WORKDIR}/dapp_*.py ${D}/opt/titania/bin
    install -m 0644 ${WORKDIR}/apps.json ${D}/opt/titania/share
}
