# TODO: SUMMARY et al.
LICENSE = "ISC"
# TODO: doesn't seem to contain a license file?
LIC_FILES_CHKSUM = "file://README.rst;md5=a4e28c1f5f7df5f5fbb1de422664f2b5"

RDEPENDS_${PN} += "fuse"

inherit pypi setuptools

SRC_URI[md5sum] = "2b9ac15c1ee854e402ed2f63039d59dd"
SRC_URI[sha256sum] = "10f5c7f5414241bffecdc333c4d3a725f1d6605cae6b4eaf86a838ff49cdaf6c"

BBCLASSEXTEND = "native nativesdk"