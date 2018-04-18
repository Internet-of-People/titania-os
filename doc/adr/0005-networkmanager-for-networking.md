# 5. NetworkManager for networking

Date: 2017-09-10

## Status

Accepted

## Context

SystemD provides native tools for managing the network connections. NetworkManager is an alternative service that provides more features and can be controlled and queried with a DBus interface. Wicd is another alternative, but is rarely used in embedded applications. There are several other options, but they are not feature full compared to NetworkManager.

## Decision

We will disable systemd network capability and use NetworkManager for managing the networks (duh!).

## Consequences

- `+` DBus interface for the configuration backend
- `+` GSM modem support for future
- `-` additional packages pulled in