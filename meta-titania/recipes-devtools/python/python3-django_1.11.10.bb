include recipes-devtools/python/python-django.inc

# Required for wsgiref
RDEPENDS_${PN} += "python3-misc"

inherit setuptools3
