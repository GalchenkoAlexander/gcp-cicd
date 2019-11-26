import logging
import copy
import json
import logging
from pathlib import Path
from typing import Tuple, Optional

import google
import requests
import requests.auth
from google.cloud import storage

from mf.config import MfFile, BuildInfo

MANIFEST_NAME = 'manifest.json'


class Storage:

    def __init__(self, bucket, semantic_name):
        credentials, _ = google.auth.default()
        self._storage_client = storage.Client(credentials=credentials)
        self._credentials = credentials
        self._semantic_name = semantic_name
        self._gs_bucket = self._storage_client.lookup_bucket(bucket)

    def fetch_manifest(self) -> Tuple[storage.bucket.Blob, dict]:
        """
        Fetch manifest from GS bucket. Remember blob's generation for concurrency control.
        :return:
        """

        bucket = self._gs_bucket
        key_ = f'{self._semantic_name}/{MANIFEST_NAME}'
        manifest_blob: storage.bucket.Blob = bucket.get_blob(key_)

        if not manifest_blob:
            raise Exception(f'{MANIFEST_NAME} not exists by key {key_} in {bucket.name}')

        str_ = manifest_blob.download_as_string()
        json_ = json.loads(str_)

        logging.info('fetching manifest blob %s', manifest_blob)
        return (manifest_blob, json_)

    def cas_blob(self, data: bytes, generation: int, bucket_name: str, blob_name: str) -> Tuple[
        bool, Optional[requests.Response]]:
        """
        Perform analog of compare-and-set operation on GoogleStorage object.

        Unfortunately google.cloud api don't provide 'if-generation-match' similar mechanics so
        JSON API was used for this purpose.

        :param bucket_name:
        :param blob_name:
        :param data: data to post
        :param generation: expected blob's generation
        :return: (true, None) - if update success;
                 (false, None) - on conflict; (false, response) - on any other http error
        """

        class AuthBearer(requests.auth.AuthBase):
            def __init__(self, t):
                self._token = t

            def __call__(self, r):
                r.headers['Authorization'] = f'Bearer {self._token}'
                return r

        # TODO add retry ?
        oauth_token = self._credentials.token
        link = f"https://storage.googleapis.com/upload/storage/v1/b/{bucket_name}/o"

        headers = {
            'x-goog-if-generation-match': str(generation)
        }

        resp = requests.post(link, data=data, params={'uploadType': 'media', 'name': blob_name},
                             headers=headers, auth=AuthBearer(oauth_token))

        if resp.status_code == 200:
            return True, None
        elif resp.status_code == 412:
            return False, None
        else:
            return False, resp

    def upload(self, bucket, key, file):
        """
        Upload file into bucket and key
        :param bucket: bucket
        :param key: key
        :param file: file
        :return:
        """
        blob: storage.client.Blob = self._storage_client.bucket(bucket).blob(key)
        logging.info("uploading %s [%s]", blob, file)
        blob.upload_from_file(file)


class Manifest(object):

    def __init__(self, bucket, repo_name):

        self._bucket = bucket
        self._repo_name = repo_name

        self._storage = Storage(bucket, repo_name)
        self.__fetch()

    def __fetch(self):
        blob, content = self._storage.fetch_manifest()

        self._content = content
        self._version = blob.generation
        self._blob_key = blob.name

    def update(self, build: BuildInfo, m_file: MfFile, upload: bool = True):
        """
        Compare and update blob by generation.
        Trying until success.

        :param upload: to do uploading of a content, (for debug)
        :param m_file:
        :param branch_name: name of a current brunch
        :param generated_manifest: new part of a manifest

        """

        refs_upload_done = False

        while True:
            current_manifest, refs = merge_new_manifest(self._content, build, m_file)

            if not upload:
                return current_manifest

            if not refs_upload_done:
                #
                # Upload assets first and update manifest only after it.
                #
                refs_upload_done = True
                for ref in refs:
                    self._storage.upload(ref['bucket'], ref['key'], ref['file'])

            ok, err_resp = self._storage.cas_blob(data=json.dumps(current_manifest).encode('utf-8'),
                                                  generation=self._version,
                                                  bucket_name=self._bucket,
                                                  blob_name=self._blob_key)
            if ok:
                break
            elif err_resp is None:
                # TODO any logic to resolve conflict in the content ?
                logging.warning("manifest have already been modified, retry...")
                self.__fetch()
            else:
                logging.error("update failed [%s] %s", err_resp.status_code, err_resp.text)
                raise Exception('GoogleStorage update failed')



def merge_new_manifest(content, build: BuildInfo, m_file: MfFile) -> Tuple[dict, dict]:
    """
    Merge generated manifest about branch into fetched from remote.

    :param build: build info
    :param m_file: config file
    :return: resulting whole manifest and assets
    """
    current_manifest = copy.deepcopy(content)
    ns_key = '@ns'
    ns = current_manifest.get(ns_key, {})

    refs_to_upload = dict()

    def __append_ref(component: str, file: Path):
        asset = {
            'key': f'{m_file.repository}/{build.git_branch}/{build.git_sha}/{component}/{file.name}',
            'bucket': m_file.bucket,
            'file': file
        }

        if asset['key'] not in refs_to_upload:
            refs_to_upload[asset['key']] = asset

        return f'gs://{asset["bucket"]}/{asset["key"]}'

    component_dict = dict(
        [(component.name, {
            "@type": component.type,
            "@metadata": {},
            "@binaries": [{
                "@md5": md5,
                "@ref": __append_ref(component.name, file)
            } for file, md5 in component.assets]
        }) for component in m_file.components]
    )

    ns[build.git_branch] = {
        "@last_success": {
            "@built_at": build.date,
            "@rev": build.git_sha,
            "@include": component_dict
        }
    }

    if ns_key not in current_manifest:
        current_manifest[ns_key] = ns

    return current_manifest, refs_to_upload
