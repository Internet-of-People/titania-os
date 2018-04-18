# 11. Preinstallable images on data volume

Date: 2018-02-24

## Status

Accepted

Extends [2. Docker for dApps](0002-docker-for-dapps.md)

Extends [8. Dual Root with Data Volume](0008-dual-root-with-data-volume.md)

Extends [9. Docker state directory on Data Volume](0009-docker-state-directory-on-data-volume.md)

## Context

Several images must come pre-installed. Currently we ship IoP stack and Nginx out of the box. There must be a way to put the respective images on the device before the network is connected.

## Decision

Images to preinstall are built in Docker format and shipped in the data volume as `/datafs/docker/preinstall/*.tar.gz`. Image names are mangled in order to remove slashes and colons. Each bundled dapp runs depends on `image-preinstall@.service` with the filename (except for `.tar.gz`) of the image to preinstall.

## Consequences

`+` independence of underlying storage backend
`+` using a standard script in Docker source, no need to patch anything
`+` ability to specify tags and hashes(!) to download
`-` certain delay at first start up (made easier by gzip compression)
`-` base layers are not shared across images, so certain duplication may happen