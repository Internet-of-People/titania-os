# Quickstart 

```
# Update the git repos
git submodule init
git submodule update

# Show where to find bitbake
# TODO: can we make it more elegant?
export BITBAKEDIR=`pwd`/bitbake

# Set up the build environment
source openembedded-core/oe-init-build-env

# Add the layers
bitbake-layers add-layer ../meta-raspberrypi
bitbake-layers add-layer ../meta-oe/meta-oe
bitbake-layers add-layer ../meta-oe/meta-python
bitbake-layers add-layer ../meta-oe/meta-filesystems
bitbake-layers add-layer ../meta-oe/meta-networking
bitbake-layers add-layer ../meta-go
bitbake-layers add-layer ../meta-virtualization
bitbake-layers add-layer ../meta-swupdate

# TitaniaOS specific
# TODO: tweak the priority
bitbake-layers add-layer ../meta-titania

# Select Titania distro TODO: more elegant way?
echo 'DISTRO = "titania"' >> conf/local.conf

# Compile the thing
bitbake rpi-titania-image
```
