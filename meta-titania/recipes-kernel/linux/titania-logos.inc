FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
SRC_URI += "file://logo_titania_mono.pbm \
            file://logo_titania_vga16.ppm \
            file://logo_titania_clut224.ppm"

# Installing Titania logo files
# TODO: better task maaaybe?
do_compile_prepend() {
    cp ${WORKDIR}/logo_titania_mono.pbm ${S}/drivers/video/logo/logo_linux_mono.pbm
    cp ${WORKDIR}/logo_titania_vga16.ppm ${S}/drivers/video/logo/logo_linux_vga16.ppm
    cp ${WORKDIR}/logo_titania_clut224.ppm ${S}/drivers/video/logo/logo_linux_clut224.ppm
}
