# 7. Layers as Git Submodules

Date: 2017-09-10

## Status

Accepted

Extends [3. Yocto as a distro base](0003-yocto-as-a-distro-base.md)

## Context

Yocto has a notion of layers which combine heterogenous code allowing to remix already usable code repositories (e.g. RaspberryPi support). There are alternative approaches on how to keep those in the project. Some advocate just forking the third party code in one's own repo. Others suggest linking their respective repos as git submodules to create dependencies.

## Decision

We will include third party layers in the repository as git submodules. We will not modify the third party layer code directly. We will use the `pyro` branch for OpenEmbedded/Yocto as a reference point.

## Consequences

- `+` no code duplication from upstream 
- `+` own code easily separated from third party, no licensing issues
- `+` smaller footprint of the distro before the user decices to fetch submodules
- `-` when alterations are needed, Yocto `bbappend` means are to be used instead of just modifying the files in a fork
- `-` setup may be complicated for devs who are not used to submodules