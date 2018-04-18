# 6. Systemd units for dApps

Date: 2017-09-10

## Status

Accepted

Extends [2. Docker for dApps](0002-docker-for-dapps.md)

Extends [4. Systemd as an init system](0004-systemd-as-an-init-system.md)

## Context

Docker has a daemon that oversees running containers. It does not however have much functionality to it, can't automatically restart the containers, can't set up containers that must be run automatically and has a separate logging system. It's possible to write a "unit template" for systemd to run containers as system services.

## Decision

We will use systemd for running the containers. We will write a template unit that can run an arbitrary dApp with systemd templating mechanism. We will use systemd `enable/disable` symlinking functionality to allow the user to configure which services must auto-start. We will advise dApp developpers to use standard output for logging.

## Consequences

- `+` `systemd` is used to babysit containers
- `+` logs are automatically accumulated by standard means
- `+` possible to extend systemd in future for things like dependencies etc.
- `-` still need to call docker to obtain stats
- `-` need to correspond containers(ids) to running units
- `-` unit template may be overcomplicated to support the flexibility