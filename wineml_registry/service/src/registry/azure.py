import uuid
from azure.storage.blob import ContainerClient
from azure.core import exceptions

from registry.base import BaseRegistryController
from registry.exception import ModelNotFound, ModelAlreadyExists
from registry.utils import resolve_artifact_path

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


    def _download(self, model_name: str, model_version: str, namespace: str):
        artifact_path = resolve_artifact_path(
            namespace=namespace,
            model_name=model_name,
            model_version=model_version,
        )
        blob_client = self.client.get_blob_client(artifact_path)
        destination_path = str(uuid.uuid4())
        try:
            with open(destination_path, "wb") as file:
                file.write(blob_client.download_blob().readall())
            return destination_path
        except exceptions.ResourceNotFoundError:
            raise ModelNotFound(f"Model does not exist")


    def _upload(self, data: str, model_name: str, model_version: str, namespace: str, model_status: str):
        artifact_path = resolve_artifact_path(
            namespace=namespace,
            model_name=model_name,
            model_version=model_version,
        )
        metadata = {"model_status": model_status}
        blob_client = self.client.get_blob_client(artifact_path)
        try:
            blob_client.upload_blob(data, metadata=metadata)
        except exceptions.ResourceExistsError:
            raise ModelAlreadyExists(f"Model already exists")

    
    def _delete(self, model_name: str, model_version: str, namespace: str):
        artifact_path = resolve_artifact_path(
            namespace=namespace,
            model_name=model_name,
            model_version=model_version,
        )
        blob_client = self.client.get_blob_client(artifact_path)
        try:
            blob_client.delete_blob()
        except exceptions.ResourceNotFoundError:
            raise ModelNotFound(f"Model does not exist")
