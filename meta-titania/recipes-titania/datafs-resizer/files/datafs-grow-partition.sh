#!/bin/sh

# Growth of the filesystem is handled by systemd
# TODO: possibly extend to make configurable?

alias datafs_free="parted -m /dev/mmcblk0p4 print | tail -n 1 | cut -d: -f4"

# Check if there is a free space at the end of SD card
if parted -m /dev/mmcblk0 print free | tail -n 1 | grep -q ':free'; then
    echo "Old size: $(datafs_free)"

    # Grow the partition
    echo "Growing the partition."
    parted /dev/mmcblk0 resizepart 4 100%

    echo "New size: $(datafs_free)"
else
    echo "Data partition already at maximum capacity, skipping"
fi
