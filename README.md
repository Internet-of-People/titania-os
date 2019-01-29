# Quickstart 

```
# Update the git repos
git submodule init
git submodule update

# Show where to find bitbake
export BITBAKEDIR=`pwd`/bitbake

# Set up the build environment
source openembedded-core/oe-init-build-env

# Add the layers
bitbake-layers add-layer ../meta-raspberrypi \
                         ../meta-oe/meta-oe \
                         ../meta-oe/meta-python \
                         ../meta-oe/meta-filesystems \
                         ../meta-oe/meta-networking \
                         ../meta-go \
                         ../meta-virtualization \
                         ../meta-swupdate \
                         ../meta-titania

# Select Titania distro
echo 'DISTRO = "titania"' >> conf/local.conf

# Compile the thing
MACHINE=raspberrypi3 bitbake rpi-titania-image
or
MACHINE=qemux86-64 bitbake x86-titania-image
```
