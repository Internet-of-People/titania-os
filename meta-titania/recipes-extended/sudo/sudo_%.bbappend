do_install_append() {
    # Allow %wheel group to do all admin commands
    sed -i -e 's/# \(%wheel ALL=(ALL) ALL\)/\1/' ${D}${sysconfdir}/sudoers 
}