#!/bin/bash

set -e
set -u
set -o pipefail

mkdir -p /tmp/mnt_new_root
if mount | grep -w / | cut -d" " -f1 | grep -q mmcblk0p2
then
    mount /dev/mmcblk0p3 /tmp/mnt_new_root
else
    mount /dev/mmcblk0p2 /tmp/mnt_new_root
fi

if [[ -f /tmp/mnt_new_root/etc/fstab ]]
then
    cat /etc/fstab | grep "^/dev/mmcblk0p1" >> /tmp/mnt_new_root/etc/fstab  # boot
    cat /etc/fstab | grep "^/dev/mmcblk0p4" >> /tmp/mnt_new_root/etc/fstab  # datafs
else
    print ERROR: could not mount new rootfs
fi

umount /tmp/mnt_new_root
