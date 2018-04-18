# Raspberry Pi usage cheat sheet

## Determining the SD card device name

Make sure you flash on the whole drive (e.g. `/dev/sdb`) and not on a partition (`/dev/sdb1`). **Double check** the device name with a GUI tool such as Disk Utility or:

### OSX

```BASH
diskutil list
```

### Linux

```BASH
lsblk
```

## Flash the image onto the card

### OSX

```BASH
sudo dd if=/path/to/file.img of=/dev/diskX bs=$[1024*1024] 
sudo sync
```

### Linux

```BASH
sudo dd if=/path/to/file.img of=/dev/sdX bs=1M conv=fsync
```

## UART

Make sure you have a driver for PL2303 (most common USB to serial converter). **Double check** that data lines in your USB converter are 3V and not 5V. 

### Connecting UART to a Pi

The position of the pins on the converter side may vary, check the labelling beforehead.

![UART connection schematic](https://eclipsesource.com/wp-content/uploads/2012/10/FTDI-to-RasPi.png "UART connection schematic")

### Generally what pin does what?

Consult [the RPi pinout](https://pinout.xyz/)

### What if I mistake RX and TX?

No worries, you will just see nothing on the screen.

### There is no output either way, what's wrong?

You may need [to enable UART](https://www.hackster.io/fvdbosch/uart-for-serial-console-or-hat-on-raspberry-pi-3-5be0c2#toc-enable-uart-1). This can be done outside of RPi just by editing the file on the card. 

### Connecting to the console from the host PC

Install `screen` (recommended), then run:
```
screen /dev/ttyNAME 115200
```

The number is the [baud rate](https://en.wikipedia.org/wiki/Baud). You can look up the name of the device in `/dev`, it generally is called `/dev/ttyUSBN` (`N` is number) on Linux and `/dev/cu.usbserial` on OSX. 

Screen has a lot of [useful shortcuts](http://aperiodic.net/screen/quick_reference) that you may want to eventually pick up (or just look up one for exiting/detaching).

You may also want to use minicom:
```BASH
minicom -D /dev/ttyNAME -b115200
```

### `screen` immediately quits, what's wrong?

Your user may not have access to the serial devices, try `sudo`.