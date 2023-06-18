import uuid

from azure.core import exceptions
from azure.storage.blob import ContainerClient
from registry.base import BaseRegistryController
from registry.exception import ModelAlreadyExists, ModelNotFound


class AzureRegistryController(BaseRegistryController):
    def __init__(self, connection_string, container_name):
        self.connection_string = connection_string
        self.container_name = container_name

    @property
    def client(self):
        if not hasattr(self, "_client"):
            self._client = ContainerClient.from_connection_string(
                conn_str=self.connection_string,
                container_name=self.container_name,
            )
        return self._client

    def _download(self, artifact_path: str):
        blob_client = self.client.get_blob_client(artifact_path)
        destination_path = str(uuid.uuid4())
        try:
            with open(destination_path, "wb") as file:
                file.write(blob_client.download_blob().readall())
            return destination_path
        except exceptions.ResourceNotFoundError:
            raise ModelNotFound("Model does not exist")

    def _upload(
        self,
        data: str,
        artifact_path: str,
    ):
        blob_client = self.client.get_blob_client(artifact_path)
        try:
            blob_client.upload_blob(data)
        except exceptions.ResourceExistsError:
            raise ModelAlreadyExists("Model already exists")
