#!/bin/sh

# TODO: several types?

SRC="$1"
DST="/datafs/titania/config$1"

# Ensuring there is a directory
# TODO: watch out for permissions!
mkdir -p $(dirname $DST)

if [ -d $SRC ]; then
    if [ ! -d $DST ]; then 
        cp -pPR $SRC $DST
    fi
elif [ -f $SRC ]; then
    if [ ! -f $DST ]; then 
        cp -pP $SRC $DST
    fi
fi