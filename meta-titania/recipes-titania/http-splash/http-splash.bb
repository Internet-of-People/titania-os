SUMMARY = "Dummy HTTP 'server' before actual nginx starts"
LICENSE = "GPL-3.0"

SRC_URI = "file://gplv3.md \
           file://http-splash@.service \
           file://http-splash.socket \
           file://http_splash.sh \
           file://http-splash.html \
           file://stop-http-splash.conf \
          "

LIC_FILES_CHKSUM = "file://${WORKDIR}/gplv3.md;md5=f149fa3bc39a974fe62c04649f34883a"

NGINX_SERVICE="dapp@world.libertaria.nginx"

inherit systemd

FILES_${PN} = "${bindir}/http_splash.sh \
               ${systemd_unitdir}/system/http-splash@.service \
               ${systemd_unitdir}/system/http-splash.socket \
               ${datadir}/http-splash/http-splash.html \
               ${sysconfdir}/systemd/system/${NGINX_SERVICE}.service.d/stop-http-splash.conf \
              "

SYSTEMD_SERVICE_${PN} = "http-splash@.service"

do_install() {
    install -d ${D}${bindir}
    install -m 755 ${WORKDIR}/http_splash.sh ${D}${bindir}
    install -d ${D}${datadir}/http-splash
    install -m 0644 ${WORKDIR}/http-splash.html ${D}${datadir}/http-splash/

    install -d ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/http-splash@.service ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/http-splash.socket ${D}${systemd_unitdir}/system

    install -d ${D}${sysconfdir}/systemd/system/${NGINX_SERVICE}.service.d
    install -m -644 ${WORKDIR}/stop-http-splash.conf ${D}${sysconfdir}/systemd/system/${NGINX_SERVICE}.service.d
}
