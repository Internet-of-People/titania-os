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
bitbake-layers add-layer meta-raspberrypi
# bitbake-layers add-layer meta-titania # not there yet

# Compile the thing
bitbake rpi-hwup-image
```