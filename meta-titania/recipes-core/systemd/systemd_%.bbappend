# Disable resolved and networkd because we use NetworkManager
PACKAGECONFIG_remove = "resolved"
PACKAGECONFIG_remove = "networkd"

# Disable sysusers because we don't need 'kvm' and 'render' groups
# and creating those groups mess up /etc/group symlink
PACKAGECONFIG_remove = "sysusers"


# systemd install script hardcodes the link for /etc/resolv.conf
# Make it point to networkmanager insted
# TODO: do we really need to? Any better way?
do_install_append() {
    # TODO: maybe just remove th line altogether
    # and only rely on update-alternatives?
    sed -i -e "s%^L! /etc/resolv.conf.*$%L! /etc/resolv.conf - - - - /run/NetworkManager/resolv.conf%g" ${D}${exec_prefix}/lib/tmpfiles.d/etc.conf

    # Prevent getty@.service from clearing the screen allowing us to see the boot log
    # and the awesome bootup logos with Titania
    sed -i -e 's/\(TTYVTDisallocate\)=yes/\1=no/' ${D}${systemd_unitdir}/system/getty@.service
}
