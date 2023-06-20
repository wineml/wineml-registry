import logging
from abc import ABC
from datetime import datetime
from typing import List

from db.schema import Model, ModelVersion, SQLModel, Tag
from schemas import ModelData, ModelVersionData
from sqlalchemy import func
from sqlmodel import Session, create_engine, select


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

    def model_exists(
        self,
        namespace: str,
        model_name: str,
    ):
        count_query = select([func.count(Model.id)]).where(
            Model.namespace == namespace,
            Model.model_name == model_name,
        )
        with Session(self.engine) as session:
            results_len = session.exec(count_query).one()
            if results_len > 0:
                return True
            else:
                return False

    def create_model(
        self,
        namespace: str,
        model_name: str,
        tags: List[str] = [],
    ):
        print(tags)
        model = Model(
            namespace=namespace,
            model_name=model_name,
            tags=[Tag(name=tag) for tag in tags],
        )
        with Session(self.engine) as session:
            session.add(model)
            session.commit()
            session.refresh(model)
            return model.id

    def get_model_id(
        self,
        namespace: str,
        model_name: str,
    ):
        count_query = select([func.count(Model.id)]).where(
            Model.namespace == namespace,
            Model.model_name == model_name,
        )
        id_query = select(Model.id).where(
            Model.namespace == namespace,
            Model.model_name == model_name,
        )
        with Session(self.engine) as session:
            results_len = session.exec(count_query).one()

            if results_len > 1:
                raise Exception("More than 1 model found")
            elif results_len == 0:
                raise Exception("No model found")
            else:
                return session.exec(id_query).first()

    def get_model(self, model_id: str):
        model_query = select(Model).where(
            Model.id == model_id,
        )
        with Session(self.engine) as session:
            model_result = session.exec(model_query).first()
            tags = [tag.name for tag in model_result.tags]
            versions = [version.model_version for version in model_result.versions]
            return ModelData(
                id=model_result.id,
                namespace=model_result.namespace,
                model_name=model_result.model_name,
                versions=versions,
                tags=tags,
            )

    def get_all_models(self):
        model_query = select(Model)
        with Session(self.engine) as session:
            model_results = session.exec(model_query).all()
            return [
                ModelData(
                    id=model_result.id,
                    namespace=model_result.namespace,
                    model_name=model_result.model_name,
                    versions=[
                        version.model_version for version in model_result.versions
                    ],
                    tags=[tag.name for tag in model_result.tags],
                )
                for model_result in model_results
            ]

    def model_add_tag(self, model_id: str, tag: str):
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

    def model_remove_tag(self, model_id: str, tag: str):
        with Session(self.engine) as session:
            model = session.exec(select(Model).where(Model.id == model_id)).one()
            db_tag = session.exec(select(Tag).where(Tag.name == tag)).first()
            try:
                model.tags.remove(db_tag)
                session.add(db_tag)
                session.commit()
            except ValueError:
                logging.warning(f"Tag {tag} not found for model {model_id}")

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

    ######################################
    # modelversion table operations
    ######################################

    def get_model_version(
        self,
        model_id: str,
        model_version: str,
    ):
        query = select(ModelVersion).where(
            ModelVersion.model_id == model_id,
            ModelVersion.model_version == model_version,
        )
        with Session(self.engine) as session:
            model_version = session.exec(query).first()
            if model_version:
                return ModelVersionData(
                    model_id=model_version.model_id,
                    model_version=model_version.model_version,
                    model_status=model_version.model_status,
                    created_at=model_version.created_at,
                    last_updated=model_version.last_updated,
                    artifact_path=model_version.artifact_path,
                )
            else:
                return None

    def get_all_model_versions(
        self,
        model_id: str,
    ):
        query = select(ModelVersion).where(
            ModelVersion.model_id == model_id,
        )
        with Session(self.engine) as session:
            model_versions = session.exec(query).all()
            return [
                ModelVersionData(
                    model_id=model_version.model_id,
                    model_version=model_version.model_version,
                    model_status=model_version.model_status,
                    created_at=model_version.created_at,
                    last_updated=model_version.last_updated,
                    artifact_path=model_version.artifact_path,
                )
                for model_version in model_versions
            ]

    def model_version_exists(
        self,
        namespace: str,
        model_name: str,
        model_version: str,
    ):
        query = select(Model).where(
            Model.namespace == namespace,
            Model.model_name == model_name,
        )
        with Session(self.engine) as session:
            model = session.exec(query).first()
            existing_versions = [
                model_version.model_version for model_version in model.versions
            ]
            if model_version in existing_versions:
                return True
            else:
                return False

    def log_new_model_version(
        self,
        namespace: str,
        model_name: str,
        model_version: str,
        model_status: str,
        artifact_path: str,
        tags: List[str] = [],
    ):
        if not self.model_exists(
            namespace=namespace,
            model_name=model_name,
        ):
            model_id = self.create_model(
                namespace=namespace, model_name=model_name, tags=tags
            )
        else:
            model_id = self.get_model_id(
                namespace=namespace,
                model_name=model_name,
            )

        if self.model_version_exists(
            namespace=namespace,
            model_name=model_name,
            model_version=model_version,
        ):
            raise Exception("Model version already exists")

        utc_timenow = datetime.utcnow()
        modelversion = ModelVersion(
            model_id=model_id,
            model_version=model_version,
            model_status=model_status,
            artifact_path=artifact_path,
            created_at=utc_timenow,
            last_updated=utc_timenow,
        )
        with Session(self.engine) as session:
            session.add(modelversion)
            session.commit()
            session.refresh(modelversion)

    def model_version_update_status(
        self,
        model_id: str,
        model_version: str,
        model_status: str,
    ):
        query = select(ModelVersion).where(
            ModelVersion.model_id == model_id,
            ModelVersion.model_version == model_version,
        )
        with Session(self.engine) as session:
            modelversion = session.exec(query).first()
            print(f"\n{model_id} {model_version}\n{modelversion}\n")
            modelversion.model_status = model_status
            modelversion.last_updated = datetime.utcnow()
            session.add(modelversion)
            session.commit()
            session.refresh(modelversion)

    ######################################
    # user table operations
    ######################################
