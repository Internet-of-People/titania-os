#!/usr/bin/python3

import subprocess
import argparse
import glob
import json
import sys

from pathlib import Path

def merge_app_jsons(src_json_files):
    result = []
    ids = set()

    for src in src_json_files:
        content = src.read_text()
        dapps = json.loads(content)

        if not isinstance(dapps, list):
            print('{}: json file should contain a list of app entries. Ignoring file.'.format(src.name), file=sys.stderr)
            continue

        for dapp in dapps:
            if dapp['id'] in ids:
                print('Warning: {src_file}: duplicate dApp ID found, ignoring dapp: {dapp_id}'.format(
                                dapp_id=dapp['id'], src_file=src.name), file=sys.stderr)
                continue

            ids.add(dapp['id'])
            result.append(dapp)

    appjson = json.dumps(result, indent=4, sort_keys=True)
    Path(args.output).write_text(appjson)

def merge(args):
    src_json_files = []
    for src_dir in args.dir:
        print('Using directory:', src_dir)
        src_dir_path = Path(src_dir)
        if not src_dir_path.exists():
            src_dir_path.mkdir(parents=True, exist_ok=True)
        
        files_here = list(src_dir_path.glob('*.json'))

        src_json_files.extend(files_here)

    for src_file in args.file:
        src_json_files.append(Path(src_file))

    print('Files:', src_json_files)

    merge_app_jsons(src_json_files)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='merge dApp json files')

    parser.add_argument('--file', type=str, nargs='*', help='use given dApp .json file as source', default=[])
    parser.add_argument('--dir', type=str, nargs='*', help='use all dApp .json files in given directories as source', default=[])
    parser.add_argument('--output', type=str, help='output filename, the merged dApp .json file', required=True)
    parser.add_argument('--inotify', action="store_true", help='keep running and watch for changes')

    args = parser.parse_args()

    merge(args)

    if args.inotify:
        # Notify systemd only if --inotify is not given and the program keeps running after merging the json files
        subprocess.run(['systemd-notify', 'READY=1'])

        while True:
            subprocess.run(['inotifywait', '-r', '-e', 'modify,attrib,delete,create,move'] + args.dir + args.file)
            print('change detected')

            while True:
                # In case an editor is writing a temporary file and moving it to the final place
                # there might be more inotify events occurring. This loop ensures there's no
                # change for a second before merging the json files to avoid interference.
                result = subprocess.run(['inotifywait', '-r', '-e', 'modify,attrib,delete,create,move', '--timeout', '1'] + args.dir + args.file)
                if result.returncode == 2:  # Timeout reached
                    break

            print('merging dApp json files')
            merge(args)

            subprocess.run(['systemctl', 'restart', 'dapp-systemd-bridge.service'])
