from datetime import datetime

from pydantic import BaseModel


class ModelData(BaseModel):
    id: int
    namespace: str
    model_name: str
    model_version: str
    model_status: str
    created_at: datetime
    last_updated: datetime
    artifact_path: str
    tags: list = []

    class Config:
        orm_mode = True
