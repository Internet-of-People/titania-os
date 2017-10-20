# Continous integration cheat sheet

This document is meant as an aide-memoire for how to deal with the images that GitLab's CI creates for us.

## Idea of the build process
GitLab builds Titania in several stages, that come *sequentially*. The workspace is reinitialized each time, but the output is saved as what GitLab calls artifacts. Through the CI/CD interface option in the repository one can inspect and download the files produced. The files have an expiration set to keep the free space under control. As such, images are only retained for 3 days after being built. There is an option to override that for particular images in the UI.

### Setup
This consists of a stage that common for all the platforms where the build directory is initialised and the correct openembedded layers are synced and added. The artifact it produces is not supposed to be public, it's just a working directory skeleton for the further stages. So no point in downloading it.

### Build
Platform specific builds are processed *in parallel*, the output of the job is a hard drive/SD card image for the platform in question and optionally a qemu config so that it's easier to run in a virtual environemnt.

### Test [NYI]
We run each of the images in a virtual machine and run a security scanner against it, as well as execute tests when we have any.

### Sign [NYI]
Images that comply with the testing are signed with a GPG key that's passed as a secret GitLab variable. The checksums are collected as well. The artifacts of the job are the collection of checksum and digital signatures for the Build artifacts.

### Publish [NYI]
Images that complete all the stages and are supposed to go public should be saved permanently somewhere and exported to IPFS (#10).

## Where to get the images from
Every build


## Platform specific
Here be dragons, the stormborn, first of her name at al.


### Raspberry Pi
.

### Desktop
.
