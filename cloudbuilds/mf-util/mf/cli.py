import argparse
import json
import datetime
from pathlib import Path

from mf.config import DEFAULT_CONFIG_FILE, config
from mf.manifest import BuildInfo, Manifest
from mf.log import LOGGER

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--git_sha", help="A git revision checksum", required=True)
    parser.add_argument("--git_brunch", help="Current git brunch", required=True)
    parser.add_argument("--build_id", help="Current GCB id", required=True)

    parser.add_argument("--upload", help="Do not upload file", default=False, action='store_true')
    parser.add_argument("--mf_file", help="Path to config file, that describes a repository. " \
                                          "By default search for {} in the root directory for current script"
                        .format(DEFAULT_CONFIG_FILE), required=False)

    args = parser.parse_args()

    root_dir = Path('.').absolute()
    LOGGER.info(f'Set current project root dir ({root_dir})')

    conf_file = config(root_dir, args.mf_file)

    actual_manifest = Manifest(conf_file.bucket, conf_file.repository)
    # TODO: add SLUG for branch name as it is present in a gcs path
    build_info = BuildInfo(git_branch=args.git_brunch, git_sha=args.git_sha,
                           date=datetime.datetime.utcnow(), build_id=args.build_id)

    new_content = actual_manifest.update(build_info, conf_file, upload=args.upload)

    if not args.upload:
        LOGGER.info("skipping upload...")
        print(json.dumps(new_content, indent=4))

    return 0
