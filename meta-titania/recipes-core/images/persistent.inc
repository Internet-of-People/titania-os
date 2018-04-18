# Collect all the files and directories that we need to be persistent,
# Move them to /etc/rw and provide symlinks

IMAGE_PREPROCESS_COMMAND += " prepare_persistent ; "

# TODO: move that to respective packages somehow
PERSISTENT_FILES = ""
PERSISTENT_FILES += "/etc/dropbear"
PERSISTENT_FILES += "/etc/NetworkManager/system-connections"
PERSISTENT_FILES += "/etc/passwd /etc/shadow /etc/group /etc/gshadow"
PERSISTENT_FILES += "/etc/hostname"

prepare_persistent() {
    RW_ROOT="${sysconfdir}/rw"
    RW_DIR="${IMAGE_ROOTFS}${RW_ROOT}"

    mkdir -p ${RW_DIR}

    for item in ${PERSISTENT_FILES}; do
        # NOTE: all items are collected on the single level hierarchy
        # TODO: We might want to change that?
        mv ${IMAGE_ROOTFS}$item $RW_DIR
        ln -s $RW_ROOT/$(basename $item) ${IMAGE_ROOTFS}$item
    done
}
