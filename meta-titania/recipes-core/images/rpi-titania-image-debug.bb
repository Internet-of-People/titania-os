include rpi-titania-image.bb

# Ensure password unlocking in case rootfs was built with production image
EXTRA_USERS_PARAMS_remove = "usermod -L root;"
