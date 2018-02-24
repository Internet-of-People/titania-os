# By default the Docker package wildcards /usr/bin/* and /lib/systemd/*
# This prevents docker-iop and docker-dapp to collect their files properly
FILES_${PN}_remove = "${bindir}/*"
FILES_${PN} += "${bindir}/docker*"
FILES_${PN}_remove = "${systemd_unitdir}/system/*"
FILES_${PN} += "${systemd_unitdir}/system/docker*"