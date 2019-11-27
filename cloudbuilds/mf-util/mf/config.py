import base64
import datetime
import hashlib
import json
import os
from mf.log import LOGGER
from pathlib import Path

from jsonschema import validate

#
# Default configuration file name.
#
DEFAULT_CONFIG_FILE = ".mf.json"

#
# This is a jsonschema for config file
# see: https://json-schema.org/understanding-json-schema/index.html
#
_SCHEMA = {
    "type": "object",
    "properties": {
        "bucket": { "type": "string" },
        "repository": { "type": "string" },
        "components": {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string"
                    },
                    "assets": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "glob": { "type": "string" }
                            }
                        }
                    },
                }

            }
        },
    }
}


def config(root: Path, mf_file=None):
    conf_file = Path(mf_file) if mf_file else root / DEFAULT_CONFIG_FILE

    if not conf_file.exists():
        LOGGER.error("config file not exists [%s]", conf_file)
        raise Exception('config file not exists %s' % conf_file)

    LOGGER.info("reading config file [%s]", conf_file)

    with open(conf_file, 'r') as f:
        cfg = json.load(f)
        validate(instance=cfg, schema=_SCHEMA)
        file = LocalConfFile(cfg, root)
        LOGGER.info("loaded config: %s", file)
        return file


class LocalConfFile:

    def __init__(self, cfg, root):
        self._cfg = cfg
        self._root_dir = root

    @property
    def components(self):
        return [
            ComponentAssets(name, json, self._root_dir) for name, json in self._cfg['components'].items()
        ]

    @property
    def bucket(self):
        return self._cfg['bucket']

    @property
    def repository(self):
        return self._cfg['repository']

    def __repr__(self):
        return f'Config{self._cfg} '


class ComponentAssets:

    def __init__(self, name, _json, dir):
        self.name = name
        self.type = str(_json['type'])
        self._json = _json
        self._dir: Path = dir

    @property
    def assets(self):
        for asset in self._json['assets']:
            glob_ptn = asset['glob']
            for p in self._dir.glob(glob_ptn):
                path_ = Path(p)
                yield (path_, _md5(path_))


def _md5(path, chunk_size=8192) -> str:
    """
     Base64 encoded MD5 hash of a file.
     Same as GCS metadata label "Hash (md5)"
    """
    with open(path, "rb") as f:
        file_hash = hashlib.md5()
        chunk = f.read(chunk_size)
        while chunk:
            file_hash.update(chunk)
            chunk = f.read(chunk_size)

        return base64.b64encode(file_hash.digest()).decode('utf-8')


class BuildInfo(object):

    def __init__(self, git_sha: str, git_branch: str, date: datetime.datetime, build_id: str):
        self.git_sha = git_sha
        self.git_branch = git_branch
        self.date = date
        self.build_id = build_id
