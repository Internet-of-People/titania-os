# TODO: replace with HTTPS link when we go public
SRC_URI = "git://git@gitlab.libertaria.community:2200/titania/ux-titania.git;protocol=ssh \
           file://vuedj.service \
           file://start_vuedj.sh"

# Pull Python in
# TODO: remove after we move to rust (dont forget to remove the layer too)
RDEPENDS_vuedj = "python-django python-pytz python-djangorestframework"

LICENSE = "GPL-3.0"
LIC_FILES_CHKSUM = "file://LICENCE.md;md5=e44ee03c4611828cc7eb00aedbf7b349"

inherit systemd

# TODO: maybe find a more sophisticated place instead of /srv/?
do_install() {
    install -m 0755 -d ${WORKDIR}/vuedj ${D}/srv/vuedj

    install -m 0755 ${WORKDIR}/start_vuedj.sh ${D}/srv/vuedj/
    install -m 0644 ${WORKDIR}/vuedj.service ${D}${systemd_unitdir}/system
}
