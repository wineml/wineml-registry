from typing import Annotated

from db import db_connector
from fastapi import APIRouter, BackgroundTasks, Depends, UploadFile
from fastapi.responses import FileResponse
from registry import registry_connector
from registry.utils import remove_file, resolve_artifact_path

router = APIRouter(tags=["user"], prefix="/user")


####################################################################################################
# Utils
####################################################################################################


async def upload_model_to_registry(
    file: UploadFile,
    artifact_path: str,
):
    contents = await file.read()
    registry_connector.upload_model(
        contents=contents,
        artifact_path=artifact_path,
    )


async def log_new_model_to_db(
    namespace: str,
    model_name: str,
    model_version: str,
    model_status: str,
    artifact_path: str,
    tags: list[str],
):
    db_connector.log_new_model(
        namespace=namespace,
        model_name=model_name,
        model_version=model_version,
        model_status=model_status,
        artifact_path=artifact_path,
        tags=tags,
    )


async def get_model_id(
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


####################################################################################################
# API
####################################################################################################


@router.get("/model")
async def get_model_info(model_id: Annotated[str, Depends(get_model_id)]):
    """
    **[DONE]**\n
    """
    model = db_connector.get_model(model_id=model_id)
    return model


@router.post("/model")
async def log_new_model(
    file: UploadFile,
    namespace: str,
    model_name: str,
    model_version: str,
    model_status: str,
    tags: list[str],
):
    """
    **[DONE]**\n
    Log a new model to the database
    1. Generate uuid for the model
    2. Upload the model to the registry
    3. Log the model to the database
    4. Set uploader as the model owner
    """
    if len(tags) == 1:
        tags = tags[0].split(",")
    artifact_path = resolve_artifact_path(
        namespace=namespace,
        model_name=model_name,
        model_version=model_version,
    )
    await upload_model_to_registry(
        file=file,
        artifact_path=artifact_path,
    )
    await log_new_model_to_db(
        namespace=namespace,
        model_name=model_name,
        model_version=model_version,
        model_status=model_status,
        artifact_path=artifact_path,
        tags=tags,
    )


@router.get("/model/download")
async def download_model_pickle(
    background_tasks: BackgroundTasks,
    namespace: str,
    model_name: str,
    model_version: str,
):
    """
    **[DONE]**\n
    """
    artifact_path = resolve_artifact_path(
        namespace=namespace,
        model_name=model_name,
        model_version=model_version,
    )
    temp_file_path = registry_connector.download_model(artifact_path=artifact_path)
    file_name = artifact_path.replace("/", "__")
    headers = {"Content-Disposition": f'attachment; filename="{file_name}"'}
    background_tasks.add_task(remove_file, temp_file_path)
    return FileResponse(temp_file_path, headers=headers)


@router.put("/model/tag")
async def add_tag(model_id: Annotated[str, Depends(get_model_id)], tag: str):
    """
    **[DONE]**\n
    """
    db_connector.add_tag(model_id=model_id, tag=tag)
    return "OK", 200


@router.put("/model/untag")
async def remove_tags(model_id: Annotated[str, Depends(get_model_id)], tag: str):
    """
    **[DONE]**\n
    """
    db_connector.remove_tag(model_id=model_id, tag=tag)
    return "OK", 200


@router.put("/model/status")
async def update_model_status(
    model_id: Annotated[str, Depends(get_model_id)], model_status: str
):
    """
    **[DONE]**\n
    """
    db_connector.update_model_status(model_id=model_id, model_status=model_status)
    return "OK", 200


@router.get("/models")
async def list_models_info():
    """
    **[TODO]**\n
    """
    models = db_connector.get_all_models()
    return models
