# 3. Yocto as a distro base

Date: 2017-09-10

## Status

Accepted

Extended by [7. Layers as Git Submodules](0007-layers-as-git-submodules.md)

## Context

There are several competing mainstream solution for generating embedded Linux firmware images. Yocto (umbrella for OpenEmbedded, BitBake and a few tools) offers modular Gentoo-like distribution generator which is extensible. Buildroot offers easier `Kconfig` based setup process. Buildroot can be forked and modified, but does not have a level of abstraction/flexibility Yocto has.

## Decision

We will use Yocto/OpenEmbedded as a base for building the firmware image. 

## Consequences

- `+` good flexibility and modularity
- `+` multi-hardware support will come easier in future
- `+` requires miminal amount of host tools, so easy to deploy
- `-` high entry threshold for new devs
- `-` high storage space requirements for building
