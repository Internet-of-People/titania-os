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

## VirtualBox

The setup of TitaniaOS x86 image for [Oracle's VirtualBox VM ware](https://www.virtualbox.org/). This guide has been written for the latest tool's [5.2.22 release](http://download.virtualbox.org/virtualbox/5.2.22/).

### Adding TitaniaOS as a VM

1. Machine -> New
2. Add name, Select type as `Linux` and Version as `Other Linux (64 bit)`. Proceed with Continue.
3. Set memory as 4GB. Proceed with continue.
4. Select `Use an existing virtual hard disk file`, and choose the image file. Hit Create.
5. Double-click to start the boot. Passwordless `root` login get you in the system.

### Setup port forwarding for viewing configuration

The following steps help you forward port from your guest(titania) setup to host(main) machine.

On your titania setup, run the following command and it should give an address like 174.13.0.3

```bash
ifconfig | grep inet addr
```

1. Select your titania machine as `titania-x86` on VirtualBox. Hit Settings-> Network.
2. Select `Attach to: NAT`
3. In Advanced, click PortForwarding and now we need to add a row here.
4. Set Protocol as `TCP`, Host IP as `127.0.0.1`, Host Port as `8000`, Guest Port as the inet address we found earlier and Guest Port as `80`. Hit OK
5. You can access titania interface at `http://127.0.0.1:8000/` on your main machine.

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

Add the following lines for the default passwordless root login.

```bash
  # default user and password
  config.ssh.username = "root"
  config.ssh.password = ""
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
