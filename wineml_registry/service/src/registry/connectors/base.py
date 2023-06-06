from abc import ABC, abstractmethod

class BaseRegistryController(ABC):
    @abstractmethod
    def _download(self):
        ...

    @abstractmethod
    def _upload(self):
        ...

    @abstractmethod
    def _delete(self):
        ...

    @abstractmethod
    def _list_many(self):
        ...

    def download_model(self, artifact_path: str):
        return self._download(artifact_path)

    def upload_model(self, contents, artifact_path: str, model_status:str):
        return self._upload(contents, artifact_path, model_status)

    def delete_model(self, artifact_path: str):
        return self._delete(artifact_path)
    
    def list_model(self, artifact_path: str, **kwargs):
        return self._list_many(artifact_path, **kwargs)