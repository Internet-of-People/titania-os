# SystemD recipe doesn't know how to parse things with multiple dots
# openembedded-core `master` branch has the correct code. 
# They get replaced in a ROOTFS_POSTPROCESS command (see rpi-titania-image)
# TODO: Either backport or upgrade branch (painful!), remove this hack
ROOTFS_POSTPROCESS_COMMAND += " systemd_coma_dot ; "
UNITS_LOCATION = "${sysconfdir}/systemd/system/multi-user.target.wants"

systemd_coma_dot() {
    for i in ${IMAGE_ROOTFS}${UNITS_LOCATION}/dapp@*.service; do
        mv $i $(dirname $i)/$(basename $i | tr , .)
    done
}
