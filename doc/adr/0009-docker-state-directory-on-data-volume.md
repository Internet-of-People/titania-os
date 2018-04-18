# 9. Docker state directory on Data Volume

Date: 2017-10-09

## Status

Accepted

Extends [2. Docker for dApps](0002-docker-for-dapps.md)

Extends [8. Dual Root with Data Volume](0008-dual-root-with-data-volume.md)

Extended by [11. Preinstallable images on data volume](0011-preinstallable-images-on-data-volume.md)

## Context

Docker has a state directory that contains images and containers. Docker has a separate update mechanism for the images to that of the root filesystem and expects its state to be mutable. The dApps and their updates should logically be disconnected to the updates to the system itself.

## Decision

We will put the Docker's state directory on the read-write data volume.

## Consequences

- `+` Root filesystem can remain read-only and limited in size
- `+`/`-` Docker's ecosystem is separate from system update
