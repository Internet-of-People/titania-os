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

## Publishing the image on the Docker Hub

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
