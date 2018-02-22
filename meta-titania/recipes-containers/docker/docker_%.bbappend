DOCKER_IMAGE_PREINSTALL ?= "\
	libertaria/nginx:armv7 \
	libertaria/iop-can:latest \
	libertaria/iop-loc:latest \
	libertaria/iop-ps:latest"

DOCKER_PREINSTALL_DIR ?= "/docker/preinstall"
PACKAGES += "${PN}-preinstall"
FILES_${PN}-preinstall += "${DOCKER_PREINSTALL_DIR}/*"

DEPENDS += "curl-native jq-native ca-certificates-native"

# TODO: cache operation, don't do every run
# TODO: requires some checksum
do_install_append() {
	# curl-native has a built-in location for certificates
	# inform it where to take sysroot certificates from
	export CURL_CA_BUNDLE="${STAGING_ETCDIR_NATIVE}/ssl/certs/ca-certificates.crt"

	for image in ${DOCKER_IMAGE_PREINSTALL}; do
		# TODO: Can we make it a part of do_fetch and save to downloads?
		IMAGE_SAFE_FILENAME=$(echo $image | tr '/:' '__')
		IMAGE_DIR="${WORKDIR}/images/$IMAGE_SAFE_FILENAME"
		echo "Saving $image to $IMAGE_DIR."

	    ${S}/contrib/download-frozen-image-v2.sh $IMAGE_DIR $image
	    install -d ${D}${DOCKER_PREINSTALL_DIR}

	    # Using gzip to gain a first boot speed tradeoff over small size benefit
	    tar -czC $IMAGE_DIR -f ${D}${DOCKER_PREINSTALL_DIR}/${IMAGE_SAFE_FILENAME}.tar.gz . 
	done
}
