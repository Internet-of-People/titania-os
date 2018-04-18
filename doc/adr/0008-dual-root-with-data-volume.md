# 8. Dual Root with Data Volume

Date: 2018-02-17

## Status

Accepted

Extended by [9. Docker state directory on Data Volume](0009-docker-state-directory-on-data-volume.md)

Extended by [11. Preinstallable images on data volume](0011-preinstallable-images-on-data-volume.md)

## Context

Embedded system need a mechanism to keep the software up to date. We want updates to be atomary for the whole system as opposed to per-package approach to ease support. We want the user to have an option to re-boot in a stable version of the system in case the system update was unsuccessful either due to client side errors, miscomunication or malfunctioning release. Some configuration files must persist through updates. We want the root filesystem itself immutable so it can be checksummed and to cover some security concerns. We can achieve that by either point-mounting some files from a read-write partition or set up a read write overlay that will automatically hold all the modification without copying the underlying read-only system.

## Decision

We will set up 2 root partitions for the system one of which will be dormant and other will be active. Updates will rewrite the dormant partition and flip which one is used on next reboot. We will lock root partitions read only and bind-mount read-write configuration files over them. We will set up a read-write "data" volume/partition and expand it to the end of the disk for modifiable configuration and other data files.

## Consequences

- `+` the system always has a stable version of the OS
- `+` the root filesystem can be checksummed and locked read-only
- `+` the system configuration is separate and can easily be backed up and ported to other instances
- `+` we can designate which configs can be changed
- `-` dual root requires twice as much space for the system files
- `-` atomary updates imply that update files are very large compared to per-package approach
- `-` each modifiable config file must be identified manually
