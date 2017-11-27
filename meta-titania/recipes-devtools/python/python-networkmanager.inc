# TODO: SUMMARY et al.
LICENSE = "zlib"
LIC_FILES_CHKSUM = "file://COPYING;md5=8d8bac174bf8422b151200e6cc78ebe4"

inherit pypi

SRC_URI[md5sum] = "5fc644a65463031295c6b7dd51a0f1bd"
SRC_URI[sha256sum] = "bc36507506ad29bfdac941b0987ebd1cc9633c9a9291d7378e229e4515a0a517"

RDEPENDS_${PN} += " \
    ${PYTHON_PN}-dbus \
    ${PYTHON_PN}-six \
    "

BBCLASSEXTEND = "native nativesdk"