inherit systemd

FILESEXTRAPATHS_prepend := "${THISDIR}/../../../ux:"

LICENSE = "GPL-3.0"
LIC_FILES_CHKSUM = "file://../LICENCE.md;md5=8c40fdc41c95755623d451deddccda48"

SRC_URI = "\
           file://vuedj/monit_dashboard.py \
           file://vuedj/manage.py \
           file://vuedj/vuedj/__init__.py \
           file://vuedj/vuedj/wsgi.py \
           file://vuedj/vuedj/urls.py \
           file://vuedj/vuedj/settings.py \
           file://vuedj/common.py \
           file://vuedj/configtitania/tests.py \
           file://vuedj/configtitania/__init__.py \
           file://vuedj/configtitania/admin.py \
           file://vuedj/configtitania/models.py \
           file://vuedj/configtitania/apps.py \
           file://vuedj/configtitania/views.py \
           file://vuedj/configtitania/serializers.py \
           file://dist/index.html \
           file://dist/static/titania.png \
           file://dist/static/css/app.88d768853b40ec8b2183ffde5fd756d0.css \
           file://dist/static/img/landing-winter.ee35bd8.svg \
           file://dist/static/img/titania-Logo-port.8ed00d5.svg \
           file://dist/static/js/app.720de067053e913ba1df.js \
           file://dist/static/js/app.720de067053e913ba1df.js.map \
           file://dist/static/js/manifest.2ae2e69a05c33dfc65f8.js \
           file://dist/static/js/manifest.2ae2e69a05c33dfc65f8.js.map \
           file://dist/static/js/vendor.00347b8c0f276345b776.js \
           file://dist/static/js/vendor.00347b8c0f276345b776.js.map \
           file://LICENCE.md \
           file://ux-titania.service \
           file://monit-dashboard.service \
           file://start_ux-titania.sh"

RDEPENDS_${PN} = "python3-django \
                  python3-pytz \
                  python3-misc \
                  python3-sqlite3 \
                  python3-djangorestframework \
                  python3-python-networkmanager \
                  sqlite3"

FILES_${PN} += "/srv/ux-titania/ ${sysconfdir}/*"

SYSTEMD_SERVICE_${PN} = "ux-titania.service monit-dashboard.service"

do_install() {
    # cp is out of place here but works for now until we go Rust
    install -d ${D}/srv/ux-titania
    install -d ${D}/srv/ux-titania/dist
    cp -dr --no-preserve=ownership ${WORKDIR}/vuedj/* ${D}/srv/ux-titania
    cp -dr --no-preserve=ownership ${WORKDIR}/dist/* ${D}/srv/ux-titania/dist
    install -m 0755 ${WORKDIR}/start_ux-titania.sh ${D}/srv/ux-titania/

    install -d ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/ux-titania.service ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/monit-dashboard.service ${D}${systemd_unitdir}/system

    # Track version
    install -d ${D}${sysconfdir}
    echo 'MACHINE=${MACHINE}' >> ${D}${sysconfdir}/titania.conf
}
