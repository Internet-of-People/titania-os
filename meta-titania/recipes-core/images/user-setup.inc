# Add custom groups
inherit extrausers
EXTRA_USERS_PARAMS += "groupadd wheel;"
# Disable passwordless root for non-debug builds
# TODO: is there a standard variable for this?
EXTRA_USERS_PARAMS += "usermod -L root;"
