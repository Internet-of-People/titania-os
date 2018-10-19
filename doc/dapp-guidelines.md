# Dapp guidelines

Dapps can be added to titania's dapps hub by defining the dapp in the form of a json manifest and restarting the dapp service.

### Architectural specifications for docker build
Since titaniaOs runs on embedded devices, the dapps must be build on armv7.
This will require you to [enable qemu](https://hub.docker.com/r/multiarch/qemu-user-static/
) on your development setup.
```
docker run --rm --privileged multiarch/qemu-user-static:register --reset
```

## Steps to add a dApp on titaniaOS
1. Form a json manifest for your dapp. Refer to the [dapp guidelines](dapp-glossary.md) to add a dapp. A sample of manifest is given below.

```
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
  "image": "libertaria/navcoin:latest"
  "staticpath": "/var/www/navcoin"
  }
  ```

2. The dapp manifest should be added at ``/datafs/app.json.d/`` as a json file. Multiple dapps can be added here comma-seperated. The dapp file should have the extension `json`.
```bash
root@titania:~# cd /datafs/apps.json.d/
root@titania:/datafs/apps.json.d:~# ls
my_dapp.json
```

3. Restart the dapp-systemd-bridge.service.
```sudo systemctl restart dapp-systemd-bridge.service```

4. You should be able to see the dapp(s) you added on the dapps hub page on the titaniaOS interface
http://titania.local/#/dappshub
or at its IP on your network
http://IP-of-titania/#/dappshub

5. You can download the dapp from its side menu. Post download, the dapp will be available on
http://titania.local/dapp/your_dapp_id

### Troubleshooting

1. If the dapp isnt available on dapp store, you can verify if the dapps list refreshed by checking the combined manifest here.
```
cat /run/apps.json
```

2. To check status of your dapp
```
systemctl status dapp@your_dapp_id.service
```

3. Quick look at all docker apps status
```
docker ps -a
```