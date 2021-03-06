WIP document, nothing to see here citizen.


# General logic

Titania has 2 root partitions labeled `root_a` and `root_b` respectively. Only one root is active, other is dormant. Likewise the are 2 corresponding kernel images. `SWupdate` flashes the updated image onto a dormant partition and overwrites the respective kernel file. After a successful update, bootloader is instructed to try booting up the new root+kernel combo. Should the boot succeed, the change is made permanent. If the update process is broken, no updates to bootloader happens.

# What is not updated

So far the following is not automatically updated:
 - Device Trees
 - `u-boot` binary
 - `u-boot` boot-up script
 - Raspberry Pi config files and firmware

# Criteria of success

Boot is considered successful if none of the services failed and `systemd` was allowed to reach `multi-user.target`. A special unit is to be made which is scheduled after everything and checks if no other unit failed. If the check is positive, permantent bootloader config is written.

# `sw-description`

The file describes what to install and where. Note that roots are intentionally labeled vice versa so that `swupdate` doesn't have to flip the active root on its own.

# Boot process

The information which root/kernel combo to run is stored in `u-boot` environment variables. The location of those may differ depending on hardware, but for Raspberry Pi we use `/boot/u-boot.env` file, which is on the 1st (VFAT) partition (`/dev/mmcblk0p1`).

Variables used:
    - `active_root`: must be either `a` or `b`. Respectively the kernel to use is either `uImage-a` or `uImage-b` (RPi) with `/dev/mmcblk0p2` or `/dev/mmcblk0p3` as root partition respectively.
    - `after_update`: set if the next run would be the first run of an updated image
    - `trial_run`: set during the first run of an updated image

## `SWupdate`

On successful update `SWupdate` alternates the `active_root` variable and sets `after_update` to `1`.

## `u-boot`

- pick the image corresponding to `active_root`
- append `root=/dev/mmcblk0pX` according to `active_root` setting to kernel parameters
- if `trial_run` is set:
    - unset `trial_run`
    - swap `active_root` value
    - save the environment

- elif `after_update` is set:
    - unset `after_update`
    - set `trial_run` to `1`
    - save the environment
- boot

## `systemd`

- if `trial_run` is set
    - If all the services started up correctly:
        - unset `trial_run`
    - Otherwise
        - reboot


# Running updates

WIP!

Use the following command:
`/sbin/update_system.sh /path/to/updatefile.swu`

The partition should pick up automatically.