SUMMARY = "Collection of images that are pre-installed on Docker"
SRC_URI += "file://gplv3.md"

# or docker-native in future
# DEPENDS_${PN} = "docker"

LICENSE = "GPL-3.0"
LIC_FILES_CHKSUM = "file://${WORKDIR}/gplv3.md;md5=f149fa3bc39a974fe62c04649f34883a"

# Main package with containers
FILES_${PN} = "/.keeper"

do_install_append() {
    # Temporary measure, after we have a good way of preinstalling dockers this will go
    touch ${D}/.keeper
}

INHIBIT_PACKAGE_STRIP = "1"
