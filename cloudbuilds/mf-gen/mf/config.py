import base64
import glob
import hashlib
import json
import logging
import os
import sys
from pathlib import Path

DEFAULT_CONFIG_FILE = ".mf.json"

def config(mf_file=None):
    conf_file = mf_file

    if not conf_file:
        dir_ = os.path.dirname(os.path.abspath(os.getcwd()))
        conf_file = os.path.join(dir_, DEFAULT_CONFIG_FILE)

    if not os.path.exists(conf_file):
        logging.error("config file not exists [%s]", conf_file)
        sys.exit(1)

    logging.info("use config file [%s]", conf_file)

    with open(conf_file, 'r') as f:
        cfg = json.load(f)
        return MfFile(cfg)


class MfFile:

    def __init__(self, cfg):
        self._cfg = cfg

    @property
    def components(self):
        return [
            ComponentAssets(name, json) for name, json in self._cfg['components'].items()
        ]

    @property
    def bucket(self):
        return self._cfg['bucket']

    @property
    def repository(self):
        return self._cfg['repository']


class ComponentAssets:

    def __init__(self, name, json_):
        self.name = name
        self.type = str(json_['type'])
        self._json = json_

    @property
    def assets(self):
        for asset in self._json['assets']:
            glob_ptn = asset['glob']
            for p in glob.glob(glob_ptn):
                path_ = Path(p)
                yield (path_, _md5(path_))


def _md5(path, chunk_size=8192) -> str:
    """
     Base64 encoded MD5 hash of a file.
     Same as GS metadata key "Hash (md5)"
    """
    with open(path, "rb") as f:
        file_hash = hashlib.md5()
        chunk = f.read(chunk_size)
        while chunk:
            file_hash.update(chunk)
            chunk = f.read(chunk_size)

        return base64.b64encode(file_hash.digest()).decode('utf-8')


class BuildInfo(object):

    def __init__(self, git_sha: str, git_branch: str, date: str):
        self.git_sha = git_sha
        self.git_branch = git_branch
        self.date = date
