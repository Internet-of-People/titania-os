# TODO: do we need `saveenv` in the beginning?
# TODO: preprocess to remove whitespace/comments
# TODO: label the partitions and select by label?

# Defaulting active root to "a"
if test "${active_root}" != "a" -a "${active_root}" != "b"; then
    setenv active_root "a"
fi

# TODO: what if both trial run and after_update are set???

# Indicate we need to swap the root 
if env exists after_update; then
    echo "Update detected, tracking the next boot"
    setenv after_update
    setenv trial_run 1
# if it was a trial run and the flag is still on, clear it
elif env exists trial_run; then
    echo "Previous trial run failed, reverting to previous version"
    setenv trial_run
fi

# Commit the changes so var
saveenv

# Swap roots for trial run
if env exists trial_run; then
    if test "${active_root}" = "a"; then
        setenv active_root "b"
    else
        setenv active_root "a"
    fi
fi

# Picking the version to run
if test "${active_root}" = "b"; then
    setenv rootpart "3"
else
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
