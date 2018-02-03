FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

# Ref: https://github.com/sbabic/meta-swupdate-boards/blob/master/raspberrypi/recipes-bsp/rpi-uboot-scr/rpi-u-boot-scr.bbappend
# TODO: not enabling COMPATIBLE="" for now
# waiting for more general multiboard support elsewhere