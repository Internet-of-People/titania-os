FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI += "file://dapp@.service 	\ 
			file://nginx.service 	\
            file://iop-ps.service 	\
            file://iop-can.service 	\
            file://iop-loc.service"

DOCKER_IMAGE_PREINSTALL ?= "\
	libertaria/nginx:armv7 \
	libertaria/iop-can:latest \
	libertaria/iop-loc:latest \
	libertaria/iop-ps:latest"

DOCKER_PREINSTALL_DIR ?= "/docker/preinstall"
# TODO: remove docker-iop after generalisation with docker-dapp
PACKAGES += "${PN}-preinstall ${PN}-iop ${PN}-dapp"
FILES_${PN}-preinstall = "${DOCKER_PREINSTALL_DIR}/*"

FILES_${PN}-dapp = "${bindir}/dapp-runner.sh 									\
					${bindir}/preinstall_docker_images.sh						\
				    ${systemd_unitdir}/system/dapp@.service 					\
				    ${systemd_unitdir}/system/preinstall-docker-images.service 	\
				   	${systemd_unitdir}/system/nginx.service"
SYSTEMD_SERVICE_${PN}-dapp = "nginx.service preinstall-docker-images.service"

FILES_${PN}-iop = "${systemd_unitdir}/system/iop-*.service"
SYSTEMD_SERVICE_${PN}-iop = "iop-ps.service 	\
							 iop-can.service 	\
							 iop-loc.service"

DEPENDS += "curl-native jq-native ca-certificates-native"

# TODO: cache operation, don't do every run
# TODO: requires some checksum
do_install_append() {
	install -d ${D}${systemd_unitdir}/system
    
	# Dapp Runner
	install -d ${D}${bindir}
    install -m 755 ${WORKDIR}/dapp-runner.sh ${D}${bindir}

    install -m 0644 ${WORKDIR}/dapp@.service ${D}${systemd_unitdir}/system

    # IoP
    install -m 0644 ${WORKDIR}/nginx.service ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/iop-*.service ${D}${systemd_unitdir}/system

	# Preinstalled images

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
