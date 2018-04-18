# 4. Systemd as an init system

Date: 2017-09-10

## Status

Accepted

Extended by [6. Systemd units for dApps](0006-systemd-units-for-dapps.md)

## Context

There are several choices for init systems. Traditional `sysvinit` uses plain shell scripts for start-up services. OpenRC is a modern reimplementation of the same with some advanced features such as dependency tracking. SystemD is a standalone native application which uses service (unit) descriptions instead of shell scripts and takes on the roles of many standard UNIX services such as logging and network configuration.
  
Ubuntu-derived upstart is similar to systemd in ideas but sort of discontinued at least for embedded applications. 

## Decision

We will use `systemd` for an init system.

## Consequences

- `+` less fragility in startup process
- `+` native support for lazy service loading and lazy mounts
- `+` one package to replace `init`, `syslog`, `cron` etc et. al
- `+` very good dependency tracking for services
- `-` some devs emotionally hate `systemd`
- `-` will need to write glue code for some packages
- `-` some devs are not used to its layout and config
