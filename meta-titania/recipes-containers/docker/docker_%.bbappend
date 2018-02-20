DOCKER_IMAGE_PREINSTALL ?= "\
	libertaria/nginx:armv7 \
	libertaria/iop-can:latest \
	libertaria/iop-loc:latest \
	libertaria/iop-ps:latest"

FILES_${PN} += "/images/*"
DEPENDS += "curl-native jq-native"

# TODO: cache operation, don't do every run
# TODO: requires some checksum
do_install_append() {
	for image in ${DOCKER_IMAGE_PREINSTALL}; do
		# TODO: Can we make it a part of do_fetch and save to downloads?
		IMAGE_DIR="${WORKDIR}/images/$(echo $image | tr '/:' '__')"
		echo "Saving $image to $IMAGE_DIR."
		
	    ${S}/contrib/download-frozen-image-v2.sh $IMAGE_DIR $image
	    install -d ${D}/images/
	    cp -r $IMAGE_DIR ${D}/images/ 
	done
}
