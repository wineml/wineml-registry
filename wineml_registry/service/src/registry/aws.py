import uuid

import boto3
from registry.base import BaseRegistryController


class AWSRegistryController(BaseRegistryController):
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name

    @property
    def client(self):
        if not hasattr(self, "_client"):
            session = boto3.Session()
            self._client = session.client("s3")
        return self._client

    def _download(self, artifact_path: str):
        destination_path = str(uuid.uuid4())
        self.client.download_file(
            Bucket=self.bucket_name,
            Key=artifact_path,
            Filename=destination_path,
        )
        return destination_path

    def _upload(
        self,
        contents: str,
        artifact_path: str,
    ):
        self.client.put_object(
            Body=contents,
            Bucket=self.bucket_name,
            Key=artifact_path,
        )
