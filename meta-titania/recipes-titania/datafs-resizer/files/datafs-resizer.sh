#!/bin/sh

# Check if there is a free space at the end of SD card
if parted /dev/mmcblk0 print free | tail -n 2 | grep -q 'Free Space'; then
    echo "Old size: "$(parted /dev/mmcblk0p4 print | tail -n 2 | awk '{ print $4; }')

    # Check if mmcblk0p4 is mounted, shouldn't be, but just in case
    if mount | grep -q /dev/mmcblk0p4 ; then
        umount /dev/mmcblk0p4
    fi

    # Grow the partition
    parted /dev/mmcblk0 resizepart 4 100%

    # Grow the filesystem
    resize2fs /dev/mmcblk0p4

    # Check the filesystem just in case
    fsck -y /dev/mmcblk0p4

    echo "New size: "$(parted /dev/mmcblk0p4 print | tail -n 2 | awk '{ print $4; }')
fi
