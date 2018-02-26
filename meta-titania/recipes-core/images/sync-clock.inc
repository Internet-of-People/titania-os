# Touch /var/lib/systemd/clock (location hardcoded in binary!) to the time of the build
# so that the clock is more reasonably initialized
ROOTFS_POSTPROCESS_COMMAND += " update_systemd_clock ; "

update_systemd_clock() {
    # TODO: WARNING: this seems to be /var/lib/systemd/timesync/clock in recent versions
    # update if the problem resurfaces
    touch ${IMAGE_ROOTFS}/var/lib/systemd/clock
}
