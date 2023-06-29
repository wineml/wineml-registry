import uuid

from google.cloud import storage
from registry.base import BaseRegistryController


class GCPRegistryController(BaseRegistryController):
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name

    @property
    def client(self):
        if not hasattr(self, "_client"):
            self._client = storage.Client()
        return self._client

    def _download(self, artifact_path: str):
        destination_path = str(uuid.uuid4())
        bucket = self.client.get_bucket(self.bucket_name)
        blob = bucket.blob(artifact_path)
        blob.download_to_filename(destination_path)
        return destination_path

    def _upload(
        self,
        contents: str,
        artifact_path: str,
    ):
        bucket = self.client.get_bucket(self.bucket_name)
        blob = bucket.blob(artifact_path)
        blob.upload_from_string(contents)
