# Dapp guidelines

## Table of Contents

1. [Guidelines Setup](#guidelines-setup)
2. [Architectural specifications for docker build](#architectural-specifications-for-docker-build)
3. [Steps to add a dApp on titaniaOS](#steps-to-add-a-dapp-on-titaniaos)
    1. [Form a json manifest for your dapp](#form-a-json-manifest-for-your-dapp)
    2. [Add manifest to titania](#add-manifest-to-titania)
    3. [Restart the dapp service](#restart-the-dapp-service)
    4. [Interact with the dapp from titaniaOS interface](#interact-with-the-dapp-from-titaniaos-interface)
4. [Troubleshooting](#troubleshooting)

## Guidelines Setup

Dapps can be added to titania's dapps hub by defining the dapp in the form of a json manifest and restarting the dapp service.

## Architectural specifications for docker build

Since titaniaOs runs on embedded devices, the dapps must be build on armv7.
This will require you to [enable qemu](https://hub.docker.com/r/multiarch/qemu-user-static/
) on your development setup.

```bash
docker run --rm --privileged multiarch/qemu-user-static:register --reset
```

## Steps to add a dApp on titaniaOS

### Form a json manifest for your dapp

Refer to the [dapp guidelines](dapp-glossary.md) to add a dapp. A sample of manifest is given below.

```json
{
"id": "org.navcoin.wallet",
  "name": "NavCoin",
  "description": "NavCoin is a decentralized cryptocurrency that uses peer-to-peer technology to operate with no central authority or banks; managing transactions and the issuing of NavCoin is carried out collectively by the network. NavCoin is open-source; its design is public, nobody owns or controls NavCoin and everyone can take part.",
  "website": "https://navcoin.org/",
  "repository": "https://gitlab.libertaria.community/titania/dApp",
  "logo": "https://navcoin.org/wp-content/uploads/2017/03/logo-mark.png",
  "labels": [
    "wallet"
  ],
  "tags": [
    "community"
  ],
  
  "ports": [{
    "name": "http",
    "port": 80,
    "protocol": "tcp",
    "type": "local"
  },
    {
      "name": "https",
      "port": 443,
      "protocol": "tcp",
      "type": "local"
    },
    {
      "name": "navcoin",
      "port": 44440,
      "protocol": "tcp",
      "type": "public"
    },
    {
      "name": "rpc",
      "port": 44444,
      "protocol": "tcp",
      "type": "local"
    }],
  "env": {},
  "volumes": ["/home/stakebox/.navcoin4"],
  "image": "libertaria/navcoin:latest",
  "staticpath": "/var/www/navcoin"
  }
  ```

### Add manifest to titania

The dapp manifest should be added at ``/datafs/app.json.d/`` as a json file. Multiple dapps can be added here comma-seperated. The dapp file should have the extension `json`.

```bash
root@titania:~# cd /datafs/apps.json.d/
root@titania:/datafs/apps.json.d:~# ls
my_dapp.json
```

### Restart the dapp service

```bash
sudo systemctl restart dapp-systemd-bridge.service
```

### Interact with the dapp from titaniaOS interface

You should be able to see the dapp(s) you added on the dapps hub page on the titaniaOS interface `http://titania.local/#/dappshub` or at its IP on your network `http://IP-of-titania/#/dappshub`.

You can download the dapp from its side menu. Post download, the dapp will be available on
`http://titania.local/dapp/your_dapp_id`.

## Troubleshooting

a. If the dapp isnt available on dapp store, you can verify if the dapps list refreshed by checking the combined manifest here.

```bash
cat /run/apps.json
```

b. To check status of your dapp

```bash
systemctl status dapp@your_dapp_id.service
```

c. Quick look at all docker apps status

```bash
docker ps -a
```