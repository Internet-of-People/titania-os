FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

# Adding the patch to the URI only if we are building a non-native recipe
# TODO: I'm not sure this is elegant, look for more standard ways
do_patch_prepend() {
    if d.getVar('PN') == 'shadow':
        d.setVar('SRC_URI_append','file://0001-rw-location-for-passwd-shadow.patch')
}