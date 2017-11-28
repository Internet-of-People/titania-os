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
$ docker run -it --rm dockercat
Hello world
```





