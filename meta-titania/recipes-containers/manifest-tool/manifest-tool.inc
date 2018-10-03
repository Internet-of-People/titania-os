DESCRIPTION = "Manifest tool for Docker manifest list object creation/query"

# Template: https://blog.gopheracademy.com/advent-2015/go-in-a-yocto-project/

GO_IMPORT = "github.com/estesp/manifest-tool"

SRC_URI = "git://${GO_IMPORT};protocol=https;destsuffix=${PN}-${PV}/src/${GO_IMPORT}"
LICENSE = "Apache-2.0"
LIC_FILES_CHKSUM = "file://src/${GO_IMPORT}/LICENSE;md5=f5d1bd1d761a52ae70630173447c5e35"

FILES_${PN} += "${GOBIN_FINAL}/*"

RDEPENDS_${PN} += "bash"

inherit go