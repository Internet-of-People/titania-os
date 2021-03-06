# Monitoring for dApps

## Generalised all info:
```
docker info
```

## Rest of the info
This currently includes all the helper dApps we have for example the custom nginx container. We need to comeup with a differentiator between dApps and helper containers
#### total dApps
```
docker ps | wc -l
```
#### Running dApps
link >> https://docs.docker.com/engine/reference/commandline/ps/#filtering
```
docker ps --filter status=running | wc -l
```
Similarly, we have status value as paused and exited

## CPU, MeM and others
link >> https://www.datadoghq.com/blog/how-to-collect-docker-metrics/#network-pseudo-files
```bash
docker stats
```
```bash
CONTAINER           CPU %               MEM USAGE / LIMIT       MEM %               NET I/O             BLOCK I/O           PIDS
778d23b2dd52        0.00%               1.148 MiB / 927.3 MiB   0.12%               91.6 kB / 3 MB      0 B / 0 B           0
CONTAINER           CPU %               MEM USAGE / LIMIT       MEM %               NET I/O             BLOCK I/O           PIDS
778d23b2dd52        0.00%               1.148 MiB / 927.3 MiB   0.12%               91.6 kB / 3 MB      0 B / 0 B           0
```

Get CPU Usage

```bash
docker stats --no-stream --format '{{.Container}}\t{{.CPUPerc}}'
```

Get containers
```bash
docker ps --format '{{.ID}}\t{{.Names}}\t{{.Image}}'
```

## Uptime
Start of Titania system / start after user has configured Titania??
cat /proc/uptime

## Threads
#### Across whole titania os
One suggestion here is to include all threads. We would show ones that are being used by our OS, helper dApps and ux processes
```
echo $(( `ps axms | wc -l`  - 1))
```
Then, we could dissect this across our registered processes. We could filter out apps using pids from docker stats
