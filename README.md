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
# TODO: tweak the priority
bitbake-layers add-layer ../meta-raspberrypi \
                         ../meta-oe/meta-oe \
                         ../meta-oe/meta-python \
                         ../meta-oe/meta-filesystems \
                         ../meta-oe/meta-networking \
                         ../meta-go \
                         ../meta-virtualization \
                         ../meta-swupdate \
                         ../meta-titania

# Select Titania distro TODO: more elegant way?
echo 'DISTRO = "titania"' >> conf/local.conf

# Select target machine
echo 'MACHINE = "raspberrypi3"' >> conf/local.conf

# Select supported rpi hardware
echo 'KERNEL_DEVICETREE = "bcm2710-rpi-3-b-plus.dtb bcm2710-rpi-3-b.dtb"' >> conf/local.conf

# Compile the thing
bitbake rpi-titania-image
```
