# Expose resolv.conf link to update-alternatives engine
# TODO: consider patching upstream
inherit update-alternatives

ALTERNATIVE_${PN} = "resolv-conf"

# /var/run is a symlink, don't use it
ALTERNATIVE_TARGET[resolv-conf] = "/run/NetworkManager/resolv.conf"
ALTERNATIVE_LINK_NAME[resolv-conf] = "${sysconfdir}/resolv.conf"

# systemd link is 50, neet to strike higher
ALTERNATIVE_PRIORITY[resolv-conf] ?= "300"

# Alternative target should exist
FILES_${PN} += "/run/NetworkManager/resolv.conf"

do_install_append() {
	install -d ${D}/run/NetworkManager/
	touch ${D}/run/NetworkManager/resolv.conf
}
