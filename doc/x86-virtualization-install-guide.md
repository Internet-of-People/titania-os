# Titania x86 virtualized build install guide

## Table of Contents

1. [VirtualBox](#virtualbox)
    1. [Adding TitaniaOS as a VM](#adding-titaniaos-as-a-vm)
    2. [Setup port forwarding for viewing configuration](#setup-port-forwarding-for-viewing-configuration)
2. [Vagrant](#vagrant)
    1. [Setting up vagrant box](#setting-up-vagrant-box)
    2. [Starting the vagrant VM](#starting-the-vagrant-vm)
    3. [Accessing Guest VM](#accessing-guest-vm)
    4. [Miscellaneous](#miscellaneous)
        1. [Stop the vagrant container](#stop-the-vagrant-container)
        2. [List all vagrant containers](#list-all-vagrant-containers)
3. [VMware](#vmware)
    1. [Setup TitaniaOS on OSX](#setup-titaniaos-on-osx)
    2. [Setup TitaniaOS on Linux](#setup-titaniaos-on-linux)

## VirtualBox

The setup of TitaniaOS x86 image for [Oracle's VirtualBox VM ware](https://www.virtualbox.org/). This guide has been written for the latest tool's [5.2.22 release](http://download.virtualbox.org/virtualbox/5.2.22/).

### Adding TitaniaOS as a VM

1. Machine -> New
2. Add name, Select type as `Linux` and Version as `Other Linux (64 bit)`. Proceed with Continue.
3. Set memory as 4GB. Proceed with continue.
4. Select `Use an existing virtual hard disk file`, and choose the image file. Hit Create.
5. Select `IDE` as disk type for the Titania image.
6. Set network interface to `Bridged`. Titania will be part of your home network.
7. Double-click to start the boot.
8. Use the IP address that appears on the console to configure your Titania Box.

## Vagrant

This is a commandline virtualization tool. Latest version is downloaded from [here](https://www.vagrantup.com/downloads.html).

### Setting up vagrant box

We can make use of the existing virtualbox setup we have.

```bash
cd ~/VirtualBox\ VMs/
```

Import the box into your environment.

```bash
vagrant package --base=titania-x86 --output=titania-x86.box
```

Setup for vagrant environment

```bash
mkdir -p ~/vagrant
cp titania-x86.box ~/vagrant
cd ~/vagrant
vagrant init
```

The `init` command will create a fresh `Vagrantfile`. Now, we make edits on your vagrant environment.

Edit line 15 to add our custom box name.

```ruby
config.vm.box = "titania-vagrant.box"
```

Uncomment line 31, so that your configuration interface is available at `http://127.0.0.1:8080/`

```ruby
config.vm.network "forwarded_port", guest: 80, host: 8000, host_ip: "127.0.0.1"
```

Add the following lines for the default root login.

```bash
  # default user and password
  config.ssh.username = "root"
  config.ssh.password = "titania"
```

### Starting the vagrant VM

```bash
vagrant up
```

### Accessing Guest VM

```bash
vagrant ssh
```

### Miscellaneous

#### Stop the vagrant container

```bash
vagrant halt
```

#### List all vagrant containers

```bash
vagrant box list
```

## VMware

You can run Titania on VMware, a very common virtualization solution.
We provide installation directions to the OSX and Linux versions here.
Other platforms may function similarly.

### Setup TitaniaOS on OSX

You can install VMware Fusion from [here](https://www.vmware.com/go/getfusion).

1. Select `Create a custom virtual machine`.
2. Under `Choose OS`, select `Linux -> Other Linux 4.x or later kernel 64-bit`. Hit Continue.
3. Set `Firmware Type` as `BIOS`
4. Under `Choose a Virtual Disk`, select `Use an existing virtual disk`.
5. Select the TitaniaOS vmdk file, with `Make a separate copy of the virtual disk` option.
6. Add a name to your VM and Finish.

### Setup TitaniaOS on Linux

This scenario is tested on WMware Workstation, and it is similar in other VMware software, too.

1. Select `New Virtual Machine`. A wizard will appear.
2. Select `Custom (advanced)` Virtual Machine Configuration.
3. Select `I will install the operation system later.`
4. Use default values up until Disk Configuration.
5. Select `IDE` as Virtual Disk Type.
6. Select `Use an existing virtual disk`. Select the Titania `.vmdk` image.
7. Finish the wizard.

## Troubleshooting

Q: What should I do if I get kernel panic during boot?
A: Make sure your disk type is set to IDE.

Q: How can I log in to the Titania Box after install?
A: You can make an administrator user on the web interface.
   The address of the web interface is displayed on the console.
   The entered username and password can be used to log in to
   Titania box via SSH or console.
   Before the administrator user is created, the default root
   password is `titania` (SSH is not allowed), which is disabled
   when the administrator user was created.

