from abc import ABC, abstractmethod


class BaseRegistryController(ABC):
    @abstractmethod
    def _download(self):
        ...

    @abstractmethod
    def _upload(self):
        ...

    def upload_model(
        self,
        contents,
        artifact_path: str,
    ):
        return self._upload(
            contents=contents,
            artifact_path=artifact_path,
        )

    def download_model(
        self,
        artifact_path: str,
    ):
        return self._download(
            artifact_path=artifact_path,
        )
