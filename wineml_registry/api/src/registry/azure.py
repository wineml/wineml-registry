from azure.storage.blob import ContainerClient

from ..registry.base import BaseRegistryController


class AzureRegistryController(BaseRegistryController):
    def __init__(self, connection_string, container_name):
        self.client = self._create_client(
            connection_string=connection_string,
            container_name=container_name,
        )

    def _create_client(self, connection_string: str, container_name: str):
        try:
            client = ContainerClient.from_connection_string(
                conn_str=connection_string, container_name=container_name
            )
            return client
        except Exception as e:
            raise e

    def get_artifact(self, artifact_path: str):
        blob_client = self.client.get_blob_client(artifact_path)
        stream = blob_client.download_blob()
        return stream.readall()

    def upload_artifact(self):
        raise NotImplementedError

    def delete_artifact(self):
        raise NotImplementedError

    def list_artifacts(self):
        raise NotImplementedError
