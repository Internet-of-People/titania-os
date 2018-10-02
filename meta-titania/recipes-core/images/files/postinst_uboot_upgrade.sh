#!/bin/bash

set -e

fw_setenv fdt_addr
fw_setenv fdtaddr
fw_setenv stdout serial,vidconsole
fw_setenv stderr serial,vidconsole

rm -f /boot/bcm2708-rpi-0-w.dtb \
      /boot/bcm2708-rpi-b.dtb \
      /boot/bcm2708-rpi-b-plus.dtb \
      /boot/bcm2708-rpi-cm.dtb \
      /boot/bcm2709-rpi-2-b.dtb \
      /boot/bcm2710-rpi-cm3.dtb

rm -rf /boot/overlays
