#!/bin/sh

# Double update
if fw_printenv after_update; then
    echo "Update flag is on, deactivating it preventively"
    fw_setenv after_update
fi

# TODO: usage etc
ACTIVE_ROOT=$(fw_printenv -n active_root)
if test $? -ne 0 ; then
	echo "Error detecting currently active root"
	exit 1
fi

echo "Currently active root: ${ACTIVE_ROOT}, flashing the other one."

swupdate -v -e stable,${ACTIVE_ROOT} -i $*

# TODO: make it a part of swupdate
rm -f /tmp/swupdateprog