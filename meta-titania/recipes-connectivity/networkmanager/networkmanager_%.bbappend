# Expose resolv.conf link to update-alternatives engine
inherit update-alternatives
FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI += "file://generate-issue.sh"

ALTERNATIVE_${PN} = "resolv-conf"

ALTERNATIVE_TARGET[resolv-conf] = "/run/NetworkManager/resolv.conf"
ALTERNATIVE_LINK_NAME[resolv-conf] = "${sysconfdir}/resolv.conf"

# systemd link is 50, neet to strike higher
ALTERNATIVE_PRIORITY[resolv-conf] ?= "300"

# Alternative target should exist
FILES_${PN} += "/run/NetworkManager/resolv.conf \
                /etc/NetworkManager/dispatcher.d/generate-issue.sh \
               "
RDEPENDS_networkmanager += "bash"

do_install_append() {
    install -d ${D}/run/NetworkManager/
    touch ${D}/run/NetworkManager/resolv.conf
    install -d 0644 ${D}/etc/NetworkManager/dispatcher.d
    install -m 0755 ${WORKDIR}/generate-issue.sh ${D}/etc/NetworkManager/dispatcher.d/
}
