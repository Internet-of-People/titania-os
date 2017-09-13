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

# TODO: not there yet
# bitbake-layers add-layer ../meta-titania

# TODO: will be pulled by Titania in future
echo 'IMAGE_INSTALL_append = " docker"' >> conf/local.conf

# Compile the thing
bitbake rpi-hwup-image
```