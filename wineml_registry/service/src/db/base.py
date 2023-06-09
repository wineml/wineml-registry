from abc import ABC
from datetime import datetime
from typing import List

from db.schema import Model, ModelTag, SQLModel
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

    def list_all_tables(self):
        metadata = MetaData(bind=self.engine)
        metadata.reflect()
        table_names = metadata.sorted_tables
        return table_names

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
        query = select(Model).where(Model.id == model_id)
        with Session(self.engine) as session:
            result = session.exec(query).first()
        return result

    def get_all_models(self) -> List[Model]:
        query = select(Model)
        with Session(self.engine) as session:
            result = session.exec(query).all()
        return result

    def log_new_model(
        self,
        namespace: str,
        model_name: str,
        model_version: str,
        model_status: str,
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

    def add_tags(self, model_id: str, tags: List[str]):
        with Session(self.engine) as session:
            all_tags = [ModelTag(name=tag, model_id=model_id) for tag in tags]
            session.add_all(all_tags)
            session.commit()

    def remove_tags(self, model_id: str, tags: List[str]):
        with Session(self.engine) as session:
            session.exec(
                delete(ModelTag).where(
                    ModelTag.name.in_(tags),
                    ModelTag.model_id == model_id,
                )
            )
            session.commit()

    ######################################
    # user table operations
    ######################################
