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
):
    db_connector.log_new_model(
        namespace=namespace,
        model_name=model_name,
        model_version=model_version,
        model_status=model_status,
        artifact_path=artifact_path,
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


@router.put("/init")
async def init_model_db():
    """
    Initialize the model database. To be used during initial startup
    """
    db_connector.create_all_tables()
    table_names = [table.name for table in db_connector.list_all_tables()]
    return table_names


@router.post("/model")
async def log_new_model(
    file: UploadFile,
    model_status: str,
    model_name: str,
    model_version: str,
    namespace: str,
):
    """
    Log a new model to the database
    1. Generate uuid for the model
    2. Upload the model to the registry
    3. Log the model to the database
    4. Set uploader as the model owner
    """
    artifact_path = resolve_artifact_path(
        namespace=namespace,
        model_name=model_name,
        model_version=model_version,
    )
    upload_model_to_registry(
        file=file,
        artifact_path=artifact_path,
    )
    log_new_model_to_db(
        namespace=namespace,
        model_name=model_name,
        model_version=model_version,
        model_status=model_status,
        artifact_path=artifact_path,
    )


@router.get("/model")
async def get_model_info(model_id: Annotated[str, Depends(get_model_id)]):
    model = db_connector.get_model(model_id=model_id)
    return model


@router.get("/models")
async def list_models_info():
    models = db_connector.get_all_models()
    return models


@router.get("/model/download")
async def download_model_pickle(
    background_tasks: BackgroundTasks,
    namespace: str,
    model_name: str,
    model_version: str,
):
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
    db_connector.add_tag(model_id=model_id, tag=tag)
    return "OK", 200


@router.put("/model/untag")
async def remove_tags(model_id: Annotated[str, Depends(get_model_id)], tags: list[str]):
    db_connector.remove_tags(model_id=model_id, tags=tags)
    return "OK", 200


@router.put("/model/status")
async def update_model_status(
    model_id: Annotated[str, Depends(get_model_id)], model_status: str
):
    db_connector.update_model_status(model_id=model_id, model_status=model_status)
    return "OK", 200
