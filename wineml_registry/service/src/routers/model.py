from typing import Annotated

from db import db_connector
from fastapi import APIRouter, Depends

router = APIRouter(tags=["model"], prefix="/model")


####################################################################################################
# Utils
####################################################################################################


async def get_model_id(
    namespace: str,
    model_name: str,
):
    model_id = db_connector.get_model_id(
        namespace=namespace,
        model_name=model_name,
    )
    return model_id


####################################################################################################
# MODEL
####################################################################################################


@router.get("")
async def get_model_info(model_id: Annotated[str, Depends(get_model_id)]):
    """
    **[DONE]**\n
    """
    model = db_connector.get_model(model_id=model_id)
    return model


@router.get("/all")
async def get_all_models_info():
    """
    **[DONE]**\n
    """
    models = db_connector.get_all_models()
    return models


@router.put("/tag")
async def add_tag(model_id: Annotated[str, Depends(get_model_id)], tag: str):
    """
    **[DONE]**\n
    """
    db_connector.model_add_tag(model_id=model_id, tag=tag)
    return "OK", 200


@router.put("/untag")
async def remove_tags(model_id: Annotated[str, Depends(get_model_id)], tag: str):
    """
    **[DONE]**\n
    """
    db_connector.model_remove_tag(model_id=model_id, tag=tag)
    return "OK", 200


@router.get("/{model_id}")
async def get_model_info_by_id(model_id: str):
    """
    **[DONE]**\n
    """
    model = db_connector.get_model(model_id=model_id)
    return model
