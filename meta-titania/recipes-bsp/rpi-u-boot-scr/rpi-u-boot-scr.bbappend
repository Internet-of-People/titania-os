FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

# Ref: https://github.com/sbabic/meta-swupdate-boards/blob/master/raspberrypi/recipes-bsp/rpi-uboot-scr/rpi-u-boot-scr.bbappend
# TODO: not enabling COMPATIBLE="" for now
# waiting for more general multiboard support elsewhere

# TODO: use meta-raspberry template mechanics for boot.cmd.in pasting ${KERNEL_IMAGETYPE} maybe?
# ref: https://github.com/mark2b/meta-raspberry/blob/cb645c6e701370a230a1531bc380f83166748c56/recipes-bsp/rpi-u-boot-scr/rpi-u-boot-scr.bb#L10
# TODO: booti command for RPI3 64 bit
# TODO: basically lots of advanced per machine customisation expected here
