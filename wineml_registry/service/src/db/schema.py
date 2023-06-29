from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class TagLink(SQLModel, table=True):
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)
    model_id: Optional[int] = Field(
        default=None, foreign_key="model.id", primary_key=True
    )


class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    models: List["Model"] = Relationship(back_populates="tags", link_model=TagLink)


class ModelVersion(SQLModel, table=True):
    model_id: Optional[int] = Field(
        default=None, foreign_key="model.id", primary_key=True
    )
    model_version: str = Field(primary_key=True)
    model_status: str
    artifact_path: str
    created_at: datetime
    last_updated: datetime
    model: "Model" = Relationship(back_populates="versions")


class Model(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    namespace: str
    model_name: str
    tags: List["Tag"] = Relationship(back_populates="models", link_model=TagLink)
    versions: List["ModelVersion"] = Relationship(back_populates="model")


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    password: str
    role: str
    team: str
