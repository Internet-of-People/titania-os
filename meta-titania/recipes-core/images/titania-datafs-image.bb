SUMMARY = "Data Partition image"
IMAGE_INSTALL = "docker-preinstall"
IMAGE_LINGUAS = ""
PACKAGE_INSTALL = "${IMAGE_INSTALL}"
IMAGE_FSTYPES = "ext3"

# Remove rootfs artifacts that we don't need
# TODO: is there a way not to install them in first place?
ROOTFS_POSTPROCESS_COMMAND += " datafs_clean; "

datafs_clean() {
	# Sanity to prevent removing system files by mistake
	if ! -d ${IMAGE_ROOTFS}; then
		# TODO: OE error somehow?
		echo "IMAGE_ROOTFS is not a directory"
		echo "Preventing further operation"
		exit 1
	fi

	rm -fr ${IMAGE_ROOTFS}${sysconfdir}
	rm -fr ${IMAGE_ROOTFS}${localstatedir}
	# TODO: is there a variable for that?
	rm -fr ${IMAGE_ROOTFS}/run
}

inherit image