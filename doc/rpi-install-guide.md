# Titania armv7 rpi install guide

Follow the following steps to setup your TitaniaBox

## Table of Contents

1. [Requirements](#requirements)
2. [Preparation](#preparation)
    1. [Fresh Install](#fresh-install)
    2. [OS Upgrade](#os-upgrade)
3. [Configuration](#configuration)

## Requirements

1. Router with Internet connection (LAN, WiFi optional)
2. Raspberry Pi 3 (starter kit, optimal)
    1. Raspberry Pi - versions 3B and 3B+ are supported
    2. LAN cable
    3. MicroSD card
    4. Power cable
    5. Raspberry Pi case (optional)
    6. monitor (optional)
3. PC with microSD card slot/adapter
4. Smartphone (optional)

## Preparation

### Fresh Install

1. Download the ``rpi`` build from these release notes.
2. Either install an image burner that supports SD cards for example Etcher, or download and install software to unpack .gz files, for example WinZIP (Windows/Mac) or “xzcat” (Linux) and unpack the TitaniaOS file
3. Assemble your Raspberry Pi motherboard and the Raspberry Pi case. Don’t plug in your Raspberry Pi yet!
4. Burn TitaniaOS ``rpi`` image on your microSD card
5. Put your SD card into your PC’s SD card slot. Format your SD card, if necessary
6. Open image burner and flash the image
7. Insert the TitaniaOS SD card into your Raspberry Pi
8. Plug the power cable into both your Pi and the socket
9. Plug the LAN cable into your Pi and your router

### OS Upgrade

For TitaniaOS versions rc_3.1 and above, download the `swu` file from the release notes. Update option is available on the footer of the TitaniaOS interface. In case of update, the ux will guide you through the process, and you can skip the remaining steps.

## Configuration

If you connect your Raspberry Pi to a monitor, you can see the boot process. The next step is to configure the box with the interface. You can use your PC or smartphone for this. Based of your router settings, you should see TitaniaOS's interface in one the following ways on your browser.

1. [http://titania.local/](http://titania.local/)
2. Scan your network and go to titaniaOS's IP

You will have the configure option now. Fill out new user credentials, wifi credentials, and save. You will be directed to the TitaniaOS's dashboard.
