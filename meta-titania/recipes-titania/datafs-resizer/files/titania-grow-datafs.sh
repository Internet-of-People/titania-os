#!/bin/bash
# Grow the datafs filesystem to the end of the block device
# This is done in 2 steps: growing the partition, then the filesystem.

source /etc/titania.conf

if [[ $MACHINE = 'qemux86-64' ]]; then
    DEV=/dev/hda
    DATA_PARTITION=/dev/hda4
elif [[ $MACHINE = 'raspberrypi3' ]]; then
    DEV=/dev/mmcblk0
    DATA_PARTITION=/dev/mmcblk0p4
else
    echo Invalid machine: $MACHINE
    exit 1
fi

function datafs_free()
{
    parted -m $DATA_PARTITION print | tail -n 1 | cut -d: -f4
}

# Check if there is a free space at the end of SD card
if parted -m $DEV print free | tail -n 1 | grep -q ':free'; then
    echo "Old size: $(datafs_free)"

    # Grow the partition
    echo "Growing the partition."
    parted $DEV resizepart 4 100%

    echo "New size: $(datafs_free)"
else
    echo "Data partition already at maximum capacity, skipping"
fi

# Grow filesystem to the end of the block device.
e2fsck -f -p $DATA_PARTITION
resize2fs $DATA_PARTITION
