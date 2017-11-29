# Containerizing

This is very much a WIP document, use with caution. We outline how to wrap your dApp in a Docker container to run on Titania. Everything is subject to change as the project progresses. This is intended as a step-by-step howto. I assume we target `x64` and `armv7` architectures for now and that the host runs `x64`.

## The setup

The document is based on a sample C/C++ CMake-based application, although the general approach can be extrapolated further. The source directory I use has a following structure:
```
src
├── CMakeLists.txt
└── hello_world.c
```

Both being trivial:

```cmake
project(hello_world)
add_executable(hello_world hello_world.c)
```

```c
#include <stdio.h>

int main() {
    printf("Hello world\n");
    return 0;
}
```

## Cross compilation

To prepare the binaries for the images we need to cross-compile them for all the architectures supported. I start with `x64` which is not technically cross-compilation because our host runs the same arch, but it's a good point to start.

In order not to pollute the host system with the toolchains I will be compiling inside a Docker container using [dockcross](https://github.com/dockcross/dockcross) set of images. This is not a requirement, although it streamlines the process greatly.

### Word of caution!

`dockcross` is based on Debian and as such the application it produces will not run in `alpine`, because the latter uses `musl` as a standard C library. Pick the toolchain corresponding to the base of your final image.

### x64 Dockerfile

We will utilize a two-step setup, whereas the cross-compilation image is first included under an alias `build` as a temporary base image to compile and then we include the real base and put the compilation results over there. Greatly simplified we are left with something like this:

```docker
# Use dockcross as temporary
FROM dockcross/linux-x64 AS build

# Copy the source inside
COPY ./src /work/src
WORKDIR /work

# Commands as you normally build the project
RUN cmake ./src
RUN make

# Real base image
FROM debian

# Copy the compilation artifacts into the final image
COPY --from=build /work/hello_world /app/hello_world

# Set the starting program
ENTRYPOINT [ "/app/hello_world" ]
```

I named the file `Dockerfile.x64` because we will have multiple archs and thus need to pass the `-f` paramater to `docker build`. We can now build the image and run a container based on it. I use `-t` option to name the resulting image with a human readable name:
```
$ docker build -f Dockerfile.x64 -t dockercat .
Sending build context to Docker daemon  63.49kB
Step 1/8 : FROM dockcross/linux-x64 AS build
 ---> fe6fee8492b6
Step 2/8 : COPY ./src /work/src
 ---> 443b19988ef4
Removing intermediate container 3bf8385989fe
Step 3/8 : WORKDIR /work
 ---> 5811b1187582
Removing intermediate container 32fdfaca72bb
Step 4/8 : RUN cmake ./src
 ---> Running in 7acad34ba573
-- The C compiler identification is GNU 4.9.2
-- The CXX compiler identification is GNU 4.9.2
-- Check for working C compiler: /usr/bin/x86_64-linux-gnu-gcc
-- Check for working C compiler: /usr/bin/x86_64-linux-gnu-gcc -- works
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Detecting C compile features
-- Detecting C compile features - done
-- Check for working CXX compiler: /usr/bin/x86_64-linux-gnu-g++
-- Check for working CXX compiler: /usr/bin/x86_64-linux-gnu-g++ -- works
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Configuring done
-- Generating done
-- Build files have been written to: /work
 ---> eea05f1e4be6
Removing intermediate container 7acad34ba573
Step 5/8 : RUN make
 ---> Running in 8140310cbffc
Scanning dependencies of target hello_world
[ 50%] Building C object CMakeFiles/hello_world.dir/hello_world.c.o
[100%] Linking C executable hello_world
[100%] Built target hello_world
 ---> 5b5ff924459e
Removing intermediate container 8140310cbffc
Step 6/8 : FROM debian
 ---> 6d83de432e98
Step 7/8 : COPY --from=build /work/hello_world /app/hello_world
 ---> 8c83d25c2ac0
Removing intermediate container 6783a85edbe9
Step 8/8 : ENTRYPOINT /app/hello_world
 ---> Running in d7dbc9f1249c
 ---> 30547e87aa92
Removing intermediate container d7dbc9f1249c
Successfully built 30547e87aa92
Successfully tagged dockercat:latest
$ docker run --rm dockercat
Hello world
```

## Adding ARM

Now we can apply the same logic in making `Dockerfile.armv7`:
```docker
FROM dockcross/linux-armv7 AS build
COPY ./src /work/src
WORKDIR /work
RUN cmake ./src
RUN make
FROM arm32v7/debian
COPY --from=build /work/hello_world /app/hello_world
ENTRYPOINT [ "/app/hello_world" ]
```

Conventionally, the non-`x64` images are prefixed with the arch, therefore we can build as:
```
$ docker build -f Dockerfile.armv7 -t arm32v7/dockercat .
Sending build context to Docker daemon  73.73kB
Step 1/8 : FROM dockcross/linux-armv7 AS build
 ---> 944b200f7fa4
Step 2/8 : COPY ./src /work/src
 ---> 25e2f4eb67e7
Removing intermediate container 7bd32b5e8caf
Step 3/8 : WORKDIR /work
 ---> 568c766f19c7
Removing intermediate container 0fed04114a0f
Step 4/8 : RUN cmake ./src
 ---> Running in 234aa984cf6d
-- The C compiler identification is GNU 4.9.2
-- The CXX compiler identification is GNU 4.9.2
-- Check for working C compiler: /usr/bin/arm-linux-gnueabihf-cc
-- Check for working C compiler: /usr/bin/arm-linux-gnueabihf-cc -- works
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Detecting C compile features
-- Detecting C compile features - done
-- Check for working CXX compiler: /usr/bin/arm-linux-gnueabihf-c++
-- Check for working CXX compiler: /usr/bin/arm-linux-gnueabihf-c++ -- works
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Configuring done
-- Generating done
-- Build files have been written to: /work
 ---> e21290135c93
Removing intermediate container 234aa984cf6d
Step 5/8 : RUN make
 ---> Running in 736576bb8ce4
Scanning dependencies of target hello_world
[ 50%] Building C object CMakeFiles/hello_world.dir/hello_world.c.o
[100%] Linking C executable hello_world
[100%] Built target hello_world
 ---> d614cb06baaa
Removing intermediate container 736576bb8ce4
Step 6/8 : FROM arm32v7/debian
 ---> d635ce0c090b
Step 7/8 : COPY --from=build /work/hello_world /app/hello_world
 ---> cf80aa4ea10f
Removing intermediate container 9b9153a95d61
Step 8/8 : ENTRYPOINT /app/hello_world
 ---> Running in b0d58ee662bd
 ---> 8f7f12985f63
Removing intermediate container b0d58ee662bd
Successfully built 8f7f12985f63
Successfully tagged arm32v7/dockercat:latest
```

## Testing on a live RPi

Before we proceed with publishing the image and making it multiarch we may want to locally test the resulting image on a live Pi. To accomplish that we want to save the image to a file and load in in Titania. E.g.:
```
$ docker save arm32v7/dockercat > dockercat-arm.tar
$ scp dockercat-arm.tar root@titania.local:/tmp
dockercat-arm.tar   100%   86MB   5.8MB/s   00:15
$ ssh root@titania.local
root@titania:~# docker load < /tmp/dockercat-arm.tar
ccd48fa5ba35: Loading layer [==================================================>] 90.63 MB/90.63 MB
1893fbd496f4: Loading layer [==================================================>] 8.192 kB/8.192 kB
Loaded image: arm32v7/dockercat:latest
root@titania:~# docker run --rm arm32v7/dockercat
Hello world
```

### Note
The usage of `root` user is provisional, after the release we will have a normal user account that never the less has access to `docker` commands.

## Publishing the image(s) on the Docker Hub

Now that we've verified our image we can post in on the central repository so that Titania can download it over the network via conventional `docker pull` means.

### Note
This section assumes we use the official Docker Hub (which is the case for now) and you have an account over there. If not, please [register](https://hub.docker.com/). Throughout this section `landswellsong` refers to my username on Docker Hub.

We used the prefix notation for the local images above, but changes are you won't be able to push it this way on Docker Hub (unless you run your private repositry) therefore we can either resort to having different image names or tags. I go with the latter approach. I could theoretically have the `dockercat:latest` pointing to an ARM build, but I deem this undesirable given we also want to publish the `x64` version later on. Thus we login on Docker Hub, make a correspondence between local images and the naming we get on the Docker Hub and push:
```
$ docker login
Login with your Docker ID to push and pull images from Docker Hub. If you don't have a Docker ID, head over to https://hub.docker.com to create one.
Username: landswellsong
Password:
Login Succeeded
$ docker tag arm32v7/dockercat landswellsong/dockercat:arm32v7
$ docker push landswellsong/dockercat:arm32v7
The push refers to a repository [docker.io/landswellsong/dockercat]
1893fbd496f4: Pushed
ccd48fa5ba35: Pushed
arm32v7: digest: sha256:9f7c5ead60a4f440e7ceba343d7d7668a5b860a9387e17dd8773be39df3249d6 size: 737
```

We can now verify that Titania is aware of such image:
```
$ ssh root@titania.local
root@titania:~# docker pull landswellsong/dockercat:arm32v7
arm32v7: Pulling from landswellsong/dockercat
Digest: sha256:9f7c5ead60a4f440e7ceba343d7d7668a5b860a9387e17dd8773be39df3249d6
Status: Downloaded newer image for landswellsong/dockercat:arm32v7
root@titania:~# docker run --rm landswellsong/dockercat:arm32v7
Hello world
```

Likewise, let's tag and push the `x64` image as well:
```
$ docker tag dockercat landswellsong/dockercat:amd64
$ docker push landswellsong/dockercat:amd64
The push refers to a repository [docker.io/landswellsong/dockercat]
994c5acece31: Layer already exists
a75caa09eb1f: Layer already exists
amd64: digest: sha256:0a281953d97e405001302f62465c57d570ea7b81a150fd4d622224dcad206653 size: 737
```

## Creating a multiarch manifest

The Titania already can pull our image via the tag specification, but the user needs to be aware of the arch he is running on, which is inconvenient. For that we are going to use the [Manifest Tool](https://github.com/estesp/manifest-tool):
```
$ git clone https://github.com/estesp/manifest-tool.git
Cloning into 'manifest-tool'...
remote: Counting objects: 3275, done.
remote: Total 3275 (delta 0), reused 0 (delta 0), pack-reused 3275
Receiving objects: 100% (3275/3275), 2.27 MiB | 1.55 MiB/s, done.
Resolving deltas: 100% (1278/1278), done.
Checking connectivity... done.
$ cd manifest-tool/
$ make
docker run --rm -i  -t -v /tmp/mt/manifest-tool:/go/src/github.com/estesp/manifest-tool -w /go/src/github.com/estesp/manifest-tool golang:1.9.1 /bin/bash -c "\
        go build -ldflags \"-X main.gitCommit="90e58e5e84ae2d1d7009d7992169037b8d178782"\" -o manifest-tool github.com/estesp/manifest-tool"
Unable to find image 'golang:1.9.1' locally
1.9.1: Pulling from library/golang
...
Digest: sha256:e2be086d86eeb789460bcb48bc26e95c5b04a61fe8cf720ae1b2195d6f40edc4
Status: Downloaded newer image for golang:1.9.1
```

Now let's prepare the YML manifest that covers both of our images:
```
image: landswellsong/dockercat:latest
manifests:
    -
        image: landswellsong/dockercat:amd64
        platform:
            architecture: amd64
            os: linux
    -
        image: landswellsong/dockercat:arm32v7
        platform:
            architecture: arm
            os: linux
```

And push it:
```
$ ./manifest-tool push from-spec dockercat-multi.yml
Digest: sha256:7525c88652bb3183a501ad50f2c49adad080f6f181d438ea91a1254958f154a2 739
```

We can verify it afterwards:
```
$ ./manifest-tool inspect landswellsong/dockercat:latest
Name:   landswellsong/dockercat:latest (Type: application/vnd.docker.distribution.manifest.list.v2+json)
Digest: sha256:7525c88652bb3183a501ad50f2c49adad080f6f181d438ea91a1254958f154a2
 * Contains 2 manifest references:
1    Mfst Type: application/vnd.docker.distribution.manifest.v2+json
1       Digest: sha256:0a281953d97e405001302f62465c57d570ea7b81a150fd4d622224dcad206653
1  Mfst Length: 737
1     Platform:
1           -      OS: linux
1           - OS Vers:
1           - OS Feat: []
1           -    Arch: amd64
1           - Variant:
1           - Feature:
1     # Layers: 2
         layer 1: digest = sha256:3e17c6eae66cd23c59751c8d8f5eaf7044e0611dc5cebb12b1273be07cdac242
         layer 2: digest = sha256:708b81686504bd3905c6e29371218859f329b4c5dd4018c2774a530a33d5fa01

2    Mfst Type: application/vnd.docker.distribution.manifest.v2+json
2       Digest: sha256:9f7c5ead60a4f440e7ceba343d7d7668a5b860a9387e17dd8773be39df3249d6
2  Mfst Length: 737
2     Platform:
2           -      OS: linux
2           - OS Vers:
2           - OS Feat: []
2           -    Arch: arm
2           - Variant:
2           - Feature:
2     # Layers: 2
         layer 1: digest = sha256:0d9fbbfaa2cd8961ae50e51e7388e3a2a1a5ca2c105389b56a3a862dfe76d035
         layer 2: digest = sha256:f8130a1fdf02992b82d3d23fd2de1dfc95f6b9a51672106a649d65477ee03a61
```

Now we can pull `landswellsong/dockercat:latest` from both the host and Titania and it will select the correct image automatically.

## TODO: state and data folders


