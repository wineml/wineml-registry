from fastapi import APIRouter, BackgroundTasks, UploadFile
from fastapi.responses import FileResponse
from registry import registry_connector
from registry.utils import resolve_artifact_path, remove_file


router = APIRouter(tags=["user", "registry"], prefix="/registry")


# delete model from registry
@router.delete("/model")
async def delete_model(model_name: str, model_version: str, namespace: str):
    registry_connector.delete_model(
        namespace=namespace,
        model_name=model_name,
        model_version=model_version,
    )
    return "OK", 200


# upload model to registry
@router.post("/model")
async def upload_model(
    file: UploadFile,
    model_status: str,
    model_name: str,
    model_version: str,
    namespace: str,
):
    contents = await file.read()
    registry_connector.upload_model(
        contents=contents,
        model_status=model_status,
        model_name=model_name,
        model_version=model_version,
        namespace=namespace,
    )
    return "OK", 200


@router.get("/model")
async def download_model(
    background_tasks: BackgroundTasks,
    model_name: str,
    model_version: str,
    namespace: str,
):
    artifact_path = resolve_artifact_path(
        namespace=namespace,
        model_name=model_name,
        model_version=model_version,
    )
    temp_file_path = registry_connector.download_model(
        namespace=namespace,
        model_name=model_name,
        model_version=model_version,
    )
    file_name = artifact_path.replace("/", "__")
    headers = {'Content-Disposition': f'attachment; filename=\"{file_name}\"'}
    background_tasks.add_task(remove_file, temp_file_path)
    return FileResponse(temp_file_path, headers=headers)
