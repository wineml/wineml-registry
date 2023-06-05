from abc import ABC, abstractmethod


class BaseRegistryController(ABC):
    @abstractmethod
    def get_artifact(self):
        ...

    @abstractmethod
    def upload_artifact(self):
        ...

    @abstractmethod
    def delete_artifact(self):
        ...

    @abstractmethod
    def list_artifacts(self):
        ...
