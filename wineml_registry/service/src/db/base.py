import logging
from abc import ABC
from datetime import datetime
from typing import List

from db.schema import Model, SQLModel, Tag, TagLink
from schemas import ModelData
from sqlalchemy import MetaData, func
from sqlmodel import Session, create_engine, delete, select


class BaseModelConnector(ABC):
    def __init__(
        self,
        engine_connector_string: str,
        connect_args: dict = {},
    ):
        self.engine = create_engine(
            engine_connector_string,
            echo=True,
            connect_args=connect_args,
        )

    ######################################
    # DB level operations
    ######################################

    def create_all_tables(self):
        SQLModel.metadata.create_all(self.engine)

    ######################################
    # model table operations
    ######################################

    def get_model_id(
        self,
        namespace: str,
        model_name: str,
        model_version: str,
    ):
        count_query = select([func.count(Model.id)]).where(
            Model.namespace == namespace,
            Model.model_name == model_name,
            Model.model_version == model_version,
        )
        id_query = select(Model.id).where(
            Model.namespace == namespace,
            Model.model_name == model_name,
            Model.model_version == model_version,
        )
        with Session(self.engine) as session:
            results_len = session.exec(count_query).one()

            # raise error if more than 1 results
            if results_len > 1:
                raise Exception("More than 1 model found")
            # raise error if no results
            elif results_len == 0:
                raise Exception("No model found")
            # return model id
            else:
                return session.exec(id_query).first()

    def if_model_exists(
        self,
        namespace: str,
        model_name: str,
        model_version: str,
    ):
        count_query = select([func.count(Model.id)]).where(
            Model.namespace == namespace,
            Model.model_name == model_name,
            Model.model_version == model_version,
        )
        with Session(self.engine) as session:
            results_len = session.exec(count_query).one()
            if results_len > 0:
                return True
            else:
                return False

    def get_model(self, model_id: str):
        model_query = select(Model).where(
            Model.id == model_id,
        )
        with Session(self.engine) as session:
            model_result = session.exec(model_query).first()
            tags = [tag.name for tag in model_result.tags]
            return ModelData(
                id=model_result.id,
                namespace=model_result.namespace,
                model_name=model_result.model_name,
                model_version=model_result.model_version,
                model_status=model_result.model_status,
                created_at=model_result.created_at,
                last_updated=model_result.last_updated,
                artifact_path=model_result.artifact_path,
                tags=tags,
            )

    def filter_models(
        self,
        namespace: str = None,
        model_name: str = None,
        model_version: str = None,
        model_status: str = None,
        tags: List[str] = [],
    ):
        query = select(Model)

        if not all(
            v in [None, []]
            for v in [namespace, model_name, model_version, model_status, tags]
        ):
            if namespace:
                query = query.where(Model.namespace == namespace)
            if model_name:
                query = query.where(Model.model_name == model_name)
            if model_version:
                query = query.where(Model.model_version == model_version)
            if model_status:
                query = query.where(Model.model_status == model_status)
            if tags:
                query = query.where(Model.tags.any(Tag.name.in_(tags)))

        with Session(self.engine) as session:
            results = session.exec(query).all()
            return [
                ModelData(
                    id=result.id,
                    namespace=result.namespace,
                    model_name=result.model_name,
                    model_version=result.model_version,
                    model_status=result.model_status,
                    created_at=result.created_at,
                    last_updated=result.last_updated,
                    artifact_path=result.artifact_path,
                    tags=[tag.name for tag in result.tags],
                )
                for result in results
            ]

    def log_new_model(
        self,
        namespace: str,
        model_name: str,
        model_version: str,
        model_status: str,
        artifact_path: str,
        tags: list[str],
    ):
        if self.if_model_exists(
            namespace=namespace,
            model_name=model_name,
            model_version=model_version,
        ):
            raise Exception("Model already exists")

        utc_timenow = datetime.utcnow()
        model = Model(
            namespace=namespace,
            model_name=model_name,
            model_version=model_version,
            model_status=model_status,
            created_at=utc_timenow,
            last_updated=utc_timenow,
            artifact_path=artifact_path,
            tags=[Tag(name=tag) for tag in tags],
        )
        with Session(self.engine) as session:
            session.add(model)
            session.commit()
            session.refresh(model)

    def update_model_status(self, model_id: str, model_status: str):
        query = select(Model).where(Model.id == model_id)
        with Session(self.engine) as session:
            model = session.exec(query).first()
            model.model_status = model_status
            model.last_updated = datetime.utcnow()
            session.add(model)
            session.commit()
            session.refresh(model)

    def add_tag(self, model_id: str, tag: str):
        with Session(self.engine) as session:
            model = session.exec(select(Model).where(Model.id == model_id)).one()
            db_tag = session.exec(select(Tag).where(Tag.name == tag)).first()
            if db_tag is None:
                logging.warning(f"Tag {tag} not found, creating new tag")
                new_db_tag = Tag(name=tag)
                session.add(new_db_tag)
                session.commit()
                session.refresh(new_db_tag)
            db_tag = session.exec(select(Tag).where(Tag.name == tag)).one()
            db_tag.models.append(model)
            session.add(db_tag)
            session.commit()

    def remove_tag(self, model_id: str, tag: str):
        with Session(self.engine) as session:
            model = session.exec(select(Model).where(Model.id == model_id)).one()
            db_tag = session.exec(select(Tag).where(Tag.name == tag)).first()
            try:
                model.tags.remove(db_tag)
            except ValueError:
                logging.warning(f"Tag {tag} not found for model {model_id}")
            session.add(db_tag)
            session.commit()

    ######################################
    # user table operations
    ######################################
