#!/usr/bin/python3

import subprocess
import argparse
import hashlib
import glob
import json
import sys
import logging

logging.basicConfig()
logger = logging.getLogger('dapp-json-merge')
logger.setLevel(logging.INFO)

from pathlib import Path


def merge_app_jsons(src_json_files):
    result = []
    ids = set()
    config_hashes = {}

    for src in src_json_files:
        content = src.read_text()
        try:
            dapps = json.loads(content)
        except json.decoder.JSONDecodeError:
            logger.warn('Invalid json file: %s' % str(src))
            continue

        if isinstance(dapps, dict):
            dapps = [dapps]

        for dapp in dapps:
            if 'id' not in dapp:
                logger.warn('Invalid json file: %s: "id" must be defined for the dapp.' % str(src))
                continue

            if dapp['id'] in ids:
                print('Warning: {src_file}: duplicate dApp ID found, ignoring dapp: {dapp_id}'.format(
                                dapp_id=dapp['id'], src_file=src.name), file=sys.stderr)
                continue

            ids.add(dapp['id'])
            result.append(dapp)

            hasher = hashlib.sha512()
            hasher.update(json.dumps(dapp, indent=4, sort_keys=True).encode())
            config_hashes[dapp['id']] = hasher.digest()

    appjson = json.dumps(result, indent=4, sort_keys=True)
    Path(args.output).write_text(appjson)
    return config_hashes

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

    return merge_app_jsons(src_json_files)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='merge dApp json files')

    parser.add_argument('--file', type=str, nargs='*', help='use given dApp .json file as source', default=[])
    parser.add_argument('--dir', type=str, nargs='*', help='use all dApp .json files in given directories as source', default=[])
    parser.add_argument('--output', type=str, help='output filename, the merged dApp .json file', required=True)
    parser.add_argument('--inotify', action="store_true", help='keep running and watch for changes')

    args = parser.parse_args()

    dapp_config_hashes = merge(args)

    if args.inotify:
        # Notify systemd only if --inotify is not given and the program keeps running after merging the json files
        subprocess.run(['systemd-notify', 'READY=1'])

        while True:
            subprocess.run(['inotifywait', '-r', '-e', 'modify,attrib,delete,create,move'] + args.dir + args.file)
            logger.info('change detected')

            while True:
                # In case an editor is writing a temporary file and moving it to the final place
                # there might be more inotify events occurring. This loop ensures there's no
                # change for a second before merging the json files to avoid interference.
                result = subprocess.run(['inotifywait', '-r', '-e', 'modify,attrib,delete,create,move', '--timeout', '1'] + args.dir + args.file)
                if result.returncode == 2:  # Timeout reached
                    break

            logger.info('merging dApp json files')
            new_hashes = merge(args)

            # Provide new config files for systemd services. This also invokes `systemctl daemon-reload`.
            subprocess.run(['systemctl', 'restart', 'dapp-systemd-bridge.service'])

            app_ids = set(list(dapp_config_hashes.keys()) + list(new_hashes.keys()))
            for app_id in app_ids:

                is_active = (subprocess.Popen(['systemctl', 'is-active', 'dapp@'+app_id], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).wait() == 0)
                is_changed = (app_id not in dapp_config_hashes or app_id not in new_hashes or dapp_config_hashes[app_id] != new_hashes[app_id])
                is_enabled = (subprocess.Popen(['systemctl', 'is-enabled', 'dapp@'+app_id], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).wait() == 0)
                logger.info('%s: is_enabled: %s, is_active: %s, is_changed: %s' % (app_id, is_enabled, is_active, is_changed))

                # Stop removed ones (which are already disabled)
                if not is_enabled:
                    if is_active:
                        logger.info('stopping ' + app_id)
                        subprocess.run(['systemctl', 'stop', 'dapp@' + app_id])

                # Make sure that everything that should run (is_enabled) and the developer is working on (is_changed)
                # are started or restarted.
                elif is_changed:
                    logger.info('(re)starting ' + app_id)
                    subprocess.run(['systemctl', 'restart', 'dapp@' + app_id])

            subprocess.run(['systemctl', 'reload', 'dapp@world.libertaria.nginx'])
            dapp_config_hashes = new_hashes
