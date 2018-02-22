#!/bin/sh

for image in /datafs/preinstall/*.tar.*; do
	echo "Loading $image into docker"

	docker load -i $image && rm -f $image
done