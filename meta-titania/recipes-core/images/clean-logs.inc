# Muting verbose printk() not to flood the console
ROOTFS_POSTPROCESS_COMMAND += " titania_sysctl_config ; "

titania_sysctl_config() {
        # systemd sysctl config, add systemv if you want
        
        test -d ${IMAGE_ROOTFS}${sysconfdir}/sysctl.d && \
                echo "kernel.printk = 3 4 1 3" > ${IMAGE_ROOTFS}${sysconfdir}/sysctl.d/quiet-boot.conf
}
