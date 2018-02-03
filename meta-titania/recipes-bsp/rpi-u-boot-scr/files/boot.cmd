# TODO: do we need `saveenv` in the beginning?
# TODO: preprocess to remove whitespace/comments
# TODO: label the partitions and select by label?

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

# Check if we are just after update
# TODO: maybe add a "failed" variable that's cleared by systemd?
# if so, update swupdate.md
if env exists after_update; then
    echo "Update detected, setting previous version as fallback."
    if test "${active_root}" = "a"; then
        setenv active_root "b"
    else
        setenv active_root "a"
    fi
    setenv after_update
    saveenv

    # Setting kernel params
    setenv bootargs ${bootargs} after_update
fi
setenv bootargs ${bootargs} root=/dev/mmcblk0p${rootpart}

# Loading and starting the kernel
fatload mmc 0:1 ${kernel_addr_r} uImage_${active_root}
bootm ${kernel_addr_r} - ${fdt_addr}
