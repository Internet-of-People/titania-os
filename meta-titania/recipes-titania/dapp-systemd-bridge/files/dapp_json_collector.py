#!/usr/bin/python3

import argparse
import glob
import json
import sys
from pathlib import Path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='aggregate dApp descriptor json files')

    parser.add_argument('src_dir', type=str, nargs="*", help='possibly multiple directories with dApp json files')
    parser.add_argument('dst_file', type=str, help='filename for the unified json')

    args = parser.parse_args()

    src_json_files = []
    for src_dir in args.src_dir:
        files_here = list(Path(src_dir).glob('*.json'))

        src_json_files.extend(files_here)

    if len(src_json_files) == 0:
       raise SystemExit('No json files found in directories: {}'.format(', '.join(args.src_dir)))

    result = []
    ids = set()

    for src in src_json_files:
        content = src.read_text()
        dapps = json.loads(content)

        if not isinstance(dapps, list):
            print('Warning: "{}" dApp json should contain a list of dApp objects'.format(src.name), file=sys.stderr)
            continue

        for dapp in dapps:
            if dapp['id'] in ids:
                print('Warning: {src_file}: duplicate dApp ID found, ignoring dapp: {dapp_id}'.format(
                                dapp_id=json['id'], src_file=src.name), file=sys.stderr)
                continue

            ids.add(dapp['id'])
            result.append(dapp)

    appjson = json.dumps(result, indent=4, sort_keys=True)
    Path(args.dst_file).write_text(appjson)
