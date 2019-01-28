# Titania App Definition File

Each dapp on titaniaOs has a defined json manifest. An example of such a manifest is given below.

## Table of Contents

1. [Example](#example)
2. [Dapp Manifest Glossary](#dapp-manifest-glossary)
    1. [Id*](#id)
    2. [Image*](#image)
    3. [Meta Data](#meta-data)
    4. [Labels](#labels)
    5. [Tags*](#tags)
    6. [Ports*](#ports)
    7. [Environment Variables](#environment-variables)
    8. [Volumes and Permissions](#volumes-and-permissions)
    9. [Platforms supported](#platforms-supported)

## Example

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
  "ports": [
    {
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
    }
  ],
  "env": [],
  "volumes": ["/home/stakebox/.navcoin4"],
  "image": "libertaria/navcoin:latest"
}
```

Let us break down the above json in the following sections.

## Dapp Manifest Glossary

### Id*

There are 3 rules for identifying your dapp.

1. A unique id is required for the service.
2. App names are written in all lower case to avoid conflict with the names of classes or interfaces.
3. As companies use their reversed Internet domain name(top-down) to begin their app names—for example, com.example.myapp for a app named myapp created by a programmer at example.com.

```json
"id": "org.navcoin.wallet"
```

### Image*

The images must be available on a publically accessible docker registry like [docker-hub](https://hub.docker.com).

```json
"image": "libertaria/navcoin:latest"
```

If you want to test iterations of changes to the repo, you can use a specific hash or tag rather than latest.

```json
"image": "libertaria/navcoin:memfixes"
```

### Meta Data

These details are used as meta data for the dapp store.

* name - name of the app
* description - a short description explaining what the user is installing. And why he should install your app.
* website - the web papge where the user can find out more about the app
* repository - where the code is hosted for the app Container.
* logo - A image to display for the app. The image hosted that is reachable through the internet.

```json
"name": "NavCoin",
"description": "NavCoin is a decentralized cryptocurrency that uses peer-to-peer technology to operate with no central authority or banks; managing transactions and the issuing of NavCoin is carried out collectively by the network. NavCoin is open-source; its design is public, nobody owns or controls NavCoin and everyone can take part.",
"website": "https://navcoin.org/",
"repository": "https://gitlab.libertaria.community/titania/dApp",
"logo": "https://navcoin.org/wp-content/uploads/2017/03/logo-mark.png"
  ```

### Labels

Used to explain the function of the app.

```json
  "labels": [
    "wallet"
  ]
```

### Tags*

Used to catogorize apps.

* Helper - Apps that are required by other dapps to run.
* Core -  Apps made by the titania team that are core to titania, currently the IoP Stack.
* Community - Apps developed by the community.

Note: Dapps you add should have the community tag

```json
  "tags": [
    "community"
  ]
```

### Ports*

Ports can be exposed out of the container by defining them in the ports sections.

A port definition is made up out of 4 fields:

* name - the name of the port
* port - the port to expose
* protocol - currently we support tcp. But in future udp might be added.
* type
  * internal - this is an open port on the container, so only the host can connect to it
  * local - this port is open just for the local network that TitaniaOS is plugged into
  * public - this port is open to the Internet

*Mapping ports container ports to different port on titania is not possible at present.*

```json
"ports": [
  {
    "name": "http",
    "port": 80,
    "protocol": "tcp",
    "type": "internal"
  },
  {
    "name": "https",
    "port": 443,
    "protocol": "tcp",
    "type": "internal"
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
  }
]
```

### Environment Variables

Enviroment Variables can be injected into the container to set certain values in the container.

Titania has a couple injected into the container automatically for all containers.

* LATITUDE
* LONGITUDE
* EXTERNAL_IP

Here is an example of an environment declaration.

```json
"env": [
  {
    "name": "CLIENTPORT",
    "value": 16981,
    "description": "TCP port to serve client (i.e. end user) queries. Optional,default value: 16981"
  }
]
```

### Volumes and Permissions

If the dockerized app needs persistent storage on titania. The volumes that need to be persisted can be added.

```json
  "volumes": ["/home/stakebox/.navcoin4"],
  "volumechown": 1000
```

### Platforms supported

This param defines the platforms supported by the dapp.

```json
  "platform": ["amd64", "armv7"]
```
