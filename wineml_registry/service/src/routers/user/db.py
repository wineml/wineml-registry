from typing import Annotated
from fastapi import APIRouter, Depends
from db import db_connector


router = APIRouter(tags=["user", "db"], prefix="/db")


def get_model_id(
    namespace: str,
    model_name: str,
    model_version: str,
):
    model_id = db_connector.get_model_id(
        namespace=namespace,
        model_name=model_name,
        model_version=model_version,
    )
    return model_id


@router.put("/init")
async def init_model_db():
    db_connector.create_all_tables()
    table_names = [table.name for table in db_connector.list_all_tables()]
    return table_names


# get all models from db
@router.get("/models")
async def get_all_models():
    models = db_connector.get_all_models()
    return models


# log new model to db
@router.post("/model")
async def log_new_model(
    namespace: str,
    model_name: str,
    model_version: str,
    model_status: str,
):
    db_connector.log_new_model(
        namespace=namespace,
        model_name=model_name,
        model_version=model_version,
        model_status=model_status,
    )
    return "OK", 200


# get model data from db
@router.get("/model")
async def get_model(model_id: Annotated[str, Depends(get_model_id)]):
    model = db_connector.get_model(model_id=model_id)
    return model


# update status of model
@router.put("/model/status")
async def update_model_status(model_id: Annotated[str, Depends(get_model_id)], model_status: str):
    db_connector.update_model_status(model_id=model_id, model_status=model_status)
    return "OK", 200


# add model tags
@router.put("/model/tag")
async def add_tags(model_id: Annotated[str, Depends(get_model_id)], tags: list[str]):
    db_connector.add_tags(model_id=model_id, tags=tags)
    return "OK", 200


# remove model tags
@router.put("/model/untag")
async def remove_tags(model_id: Annotated[str, Depends(get_model_id)], tags: list[str]):
    db_connector.remove_tags(model_id=model_id, tags=tags)
    return "OK", 200