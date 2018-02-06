#!/bin/bash

# Skip if we are not in trial run
if ! fw_printenv trial_run; then
    echo "Normal run, nothing is needed"
    exit
fi


echo "Trial run detected"
# TODO: "check that none of the units failed so far"
# TODO: can we depend on all of them in systemd?

fw_setenv trial_run
