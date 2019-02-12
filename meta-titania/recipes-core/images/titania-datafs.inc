DATAFS_FILENAME ?= "titania-datafs-image-${MACHINE}.ext4"

# Cause datafs image to be built
do_image_wic[depends] += "titania-datafs-image:do_build"
