from typing import Annotated, List

from db import db_connector
from fastapi import APIRouter, BackgroundTasks, Depends, UploadFile
from fastapi.responses import FileResponse
from registry import registry_connector
from registry.utils import remove_file, resolve_artifact_path
from routers.model import get_model_id

router = APIRouter(tags=["modelversion"], prefix="/modelversion")


####################################################################################################
# Utils
####################################################################################################


async def upload_model_version_to_registry(
    file: UploadFile,
    artifact_path: str,
):
    contents = await file.read()
    registry_connector.upload_model(
        contents=contents,
        artifact_path=artifact_path,
    )


async def log_new_model_version_to_db(
    namespace: str,
    model_name: str,
    model_version: str,
    model_status: str,
    artifact_path: str,
    tags: List[str],
):
    db_connector.log_new_model_version(
        namespace=namespace,
        model_name=model_name,
        model_version=model_version,
        model_status=model_status,
        artifact_path=artifact_path,
        tags=tags,
    )


####################################################################################################
# MODEL VERSION
####################################################################################################


@router.get("")
async def get_model_version_info(
    model_id: Annotated[str, Depends(get_model_id)], model_version: str
):
    """
    **[DONE]**\n
    """
    modelversion = db_connector.get_model_version(
        model_id=model_id, model_version=model_version
    )
    return modelversion


@router.post("")
async def log_new_model_version(
    file: UploadFile,
    namespace: str,
    model_name: str,
    model_version: str,
    model_status: str,
    tags: List[str] = [],
):
    """
    **[DONE]**\n
    Log a new model to the database
    1. Generate uuid for the model
    2. Upload the model to the registry
    3. Log the model to the database
    4. Set uploader as the model owner
    """

    # workaround for body with file and json
    if tags:
        tags = list(set(tags[0].split(",")))

    artifact_path = resolve_artifact_path(
        namespace=namespace,
        model_name=model_name,
        model_version=model_version,
    )

    await upload_model_version_to_registry(
        file=file,
        artifact_path=artifact_path,
    )

    await log_new_model_version_to_db(
        namespace=namespace,
        model_name=model_name,
        model_version=model_version,
        model_status=model_status,
        artifact_path=artifact_path,
        tags=tags,
    )


@router.get("/all")
async def get_all_model_version_info(model_id: Annotated[str, Depends(get_model_id)]):
    """
    **[DONE]**\n
    """
    modelversions = db_connector.get_all_model_versions(model_id=model_id)
    return modelversions


@router.get("/download")
async def download_modelversion_pickle(
    background_tasks: BackgroundTasks,
    model_id: Annotated[str, Depends(get_model_id)],
    model_version: str,
):
    """
    **[DONE]**\n
    """
    model_version = db_connector.get_model_version(
        model_id=model_id, model_version=model_version
    )
    temp_file_path = registry_connector.download_model(
        artifact_path=model_version.artifact_path
    )
    file_name = model_version.artifact_path.replace("/", "__")
    headers = {"Content-Disposition": f'attachment; filename="{file_name}"'}
    background_tasks.add_task(remove_file, temp_file_path)
    return FileResponse(temp_file_path, headers=headers)


@router.put("/status")
async def update_model_status(
    model_id: Annotated[str, Depends(get_model_id)],
    model_version: str,
    model_status: str,
):
    """
    **[DONE]**\n
    """
    db_connector.model_version_update_status(
        model_id=model_id,
        model_version=model_version,
        model_status=model_status,
    )
    return "OK", 200
