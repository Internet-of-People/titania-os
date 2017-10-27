# Set the welcome banner to /etc/issue.net
do_install_append() {
    echo "DROPBEAR_EXTRA_ARGS=\"-b ${sysconfdir}/issue.net\"" > ${D}${sysconfdir}/default/dropbear
}
