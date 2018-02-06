# TODO: do we need `saveenv` in the beginning?
# TODO: preprocess to remove whitespace/comments
# TODO: label the partitions and select by label?

# Check if it was a failed run
if env exists trial_run; then
    echo "Previous trial run failed, reverting active partitions"
    if test "${active_root}" = "a"; then
        setenv active_root "b"
    else
        setenv active_root "a"
    fi
    setenv trial_run
    saveenv
# Check if we are just after update
elif env exists after_update; then
    echo "Update detected, tracking the next boot"
    
    setenv after_update
    setenv trial_run 1
    saveenv
fi

# Picking the version to run
if test "${active_root}" = "b"; then
    setenv rootpart "3"
else # Not "b" is interpreted as "a" and corrected
    if test "${active_root}" != "a"; then
        setenv active_root "a"
        saveenv
    fi
    setenv rootpart "2"
fi

echo "Active version: ${active_root}"
echo "Active partition: /dev/mmcblk0p${rootpart}"

# Loading FDT
fdt addr ${fdt_addr} && fdt get value bootargs /chosen bootargs
setenv bootargs ${bootargs} root=/dev/mmcblk0p${rootpart}

# Loading and starting the kernel
fatload mmc 0:1 ${kernel_addr_r} uImage_${active_root}
bootm ${kernel_addr_r} - ${fdt_addr}
