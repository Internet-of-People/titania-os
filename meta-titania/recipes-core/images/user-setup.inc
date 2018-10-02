# TODO: remove /etc/passwd- etc

# Add custom groups
inherit extrausers
EXTRA_USERS_PARAMS += "groupadd --system wheel; groupadd --non-unique --gid 65534 nobody;"
# Disable passwordless root for non-debug builds
# TODO: is there a standard variable for this?
EXTRA_USERS_PARAMS += "usermod --lock root;"
