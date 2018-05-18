#!/bin/sh

# TODO: container must to this on its own eventually
if systemctl is-active -q dapp@global.iop.loc; then
    systemctl stop dapp@global.iop.loc
fi

docker rm global.iop.loc
rm -fr /datafs/dapp/global.iop.loc
