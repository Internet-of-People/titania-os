# TODO: replace with HTTPS link when we go public
SRC_URI = "git://git@gitlab.libertaria.community:2200/titania/ux-titania.git;protocol=ssh"

# Pull Python in
# TODO: remove after we move to rust (dont forget to remove the layer too)
RDEPENDS_vuedj = "python-django python-pytz python-djangorestframework"

LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENCE.md;md5=e44ee03c4611828cc7eb00aedbf7b349"
