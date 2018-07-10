# Set the welcome banner to /etc/issue.net
do_install_append() {
    echo "DROPBEAR_EXTRA_ARGS=\"-b ${sysconfdir}/issue.net\"" > ${D}${sysconfdir}/default/dropbear
}

do_edit_options() {
    local REMOVE_OPTIONS="DROPBEAR_3DES DROPBEAR_ENABLE_CBC_MODE DROPBEAR_DSS DROPBEAR_MD5_HMAC DROPBEAR_SHA1_96_HMAC"

    local options_file=${WORKDIR}/dropbear-20*/options.h
    for feature in $REMOVE_OPTIONS; do
        if ! grep --quiet $feature $options_file; then
            echo $feature not found in options.h
            exit 1
        fi

        echo removing $feature from dropbear options.h
        sed -i "s/.*$feature\$//" $options_file

        # make sure options are actually removed
        if grep --quiet $feature $options_file; then
            echo Could not remove $feature from options.h
            exit 1
        fi
    done
}

addtask edit_options after do_configure before do_compile
