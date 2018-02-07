#!/bin/sh

# TODO: usage etc
ACTIVE_ROOT=$(fw_printenv -n active_root)
if test $? -ne 0 ; then
	echo "Error detecting currently active root"
	exit 1
fi

echo "Currently active root: ${ACTIVE_ROOT}, flashing the other one."

swupdate -v -e stable,${ACTIVE_ROOT} -i $*