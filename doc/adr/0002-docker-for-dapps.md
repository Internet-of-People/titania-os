# 2. Docker for dApps

Date: 2017-09-10

## Status

Accepted

Extended by [6. Systemd units for dApps](0006-systemd-units-for-dapps.md)

Extended by [9. Docker state directory on Data Volume](0009-docker-state-directory-on-data-volume.md)

Extended by [11. Preinstallable images on data volume](0011-preinstallable-images-on-data-volume.md)

## Context

Titania is supposed to run multiple dApps. There are multiple techologies and concepts on how to define and isolate a dApp. 

## Decision

We will use LXC technology and represent a dApp as a container. We will use Docker to build, run and manage said containers.

## Consequences

- `+` ease of development
- `+` good performance on low end hardware
- `+` compact footprint
- `-` imperfect isolation due to kernel sharing
- `-` requires more security audit
