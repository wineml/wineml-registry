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

    def delete_model(self, model_name: str, model_version: str, namespace: str):
        return self._delete(
            model_name=model_name,
            model_version=model_version,
            namespace=namespace,
        )

    def upload_model(
        self,
        contents,
        model_status: str,
        model_name: str,
        model_version: str,
        namespace: str,
    ):
        return self._upload(
            contents=contents,
            model_status=model_status,
            model_name=model_name,
            model_version=model_version,
            namespace=namespace,
        )

    def download_model(
        self,
        model_name: str,
        model_version: str,
        namespace: str,
    ):
        return self._download(
            model_name=model_name,
            model_version=model_version,
            namespace=namespace,
        )
