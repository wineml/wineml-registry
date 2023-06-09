import uuid
from sqlmodel import SQLModel, Field
from pydantic import UUID1
from datetime import datetime


class Model(SQLModel, table=True):
    id: UUID1 = Field(
        default_factory=uuid.uuid1,
        primary_key=True,
        index=True,
        nullable=False,
    )
    namespace: str
    model_name: str
    model_version: str
    model_status: str
    created_at: datetime
    last_updated: datetime


class ModelTag(SQLModel, table=True):
    name: str = Field(
        primary_key=True,
        nullable=False,
    )
    model_id: UUID1 = Field(nullable=False)


class User(SQLModel, table=True):
    id: UUID1 = Field(
        default_factory=uuid.uuid1,
        primary_key=True,
        index=True,
        nullable=False,
    )
    username: str
    email: str
    password: str
    role: str
    team: str
