from datetime import datetime

from pydantic import BaseModel


class ModelData(BaseModel):
    id: int
    namespace: str
    model_name: str
    tags: list = []
    versions: list = []

    class Config:
        orm_mode = True


class ModelVersionData(BaseModel):
    model_id: int
    model_version: str
    model_status: str
    artifact_path: str
    created_at: datetime
    last_updated: datetime

    class Config:
        orm_mode = True
