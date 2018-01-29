# TODO: SUMMARY et al.
LICENSE = "BSD"
LIC_FILES_CHKSUM = "file://LICENSE.md;md5=2eb816d2fd907ac0fae84a532cbf7b84"

inherit pypi setuptools

SRC_URI[md5sum] = "fe7f837ce0403d4ba449fad9cf557077"
SRC_URI[sha256sum] = "8ba4908d9fe4d78a8459fe86922e434006d491d4486086d23b19cd0975a3dba5"

RDEPENDS_${PN} += " \
    ${PYTHON_PN}-django \
    "

BBCLASSEXTEND = "native nativesdk"
