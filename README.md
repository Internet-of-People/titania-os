# Quickstart 

```
git submodule init
git submodule update
source openembedded-core/oe-init-build-env
bitbake-layers add-layer meta-raspberrypi
# bitbake-layers add-layer meta-titania # not there yet
bitbake rpi-hwup-image
```