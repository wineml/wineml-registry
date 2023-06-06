from fastapi import APIRouter, BackgroundTasks, UploadFile, Depends
from fastapi.responses import FileResponse
from registry import registry_client
from registry.utils import resolve_artifact_path, remove_file


router = APIRouter(tags=["user", "registry"])


@router.get("/model")
async def download_model(
    background_tasks: BackgroundTasks,
    artifact_path: str=Depends(resolve_artifact_path),
    ):
    temp_file_path = registry_client.download_model(artifact_path)
    file_name = artifact_path.replace("/", "__")
    headers = {'Content-Disposition': f'attachment; filename=\"{file_name}\"'}
    background_tasks.add_task(remove_file, temp_file_path)
    return FileResponse(temp_file_path, headers=headers)


@router.delete("/model")
async def delete_model(artifact_path: str=Depends(resolve_artifact_path)):
    registry_client.delete_model(artifact_path)
    return "OK", 200


@router.post("/model")
async def upload_model(
    file: UploadFile,
    model_status: str="experimental",
    artifact_path: str=Depends(resolve_artifact_path),
    ):
    contents = await file.read()
    registry_client.upload_model(contents, artifact_path, model_status)
    return "OK", 200


@router.get("/models")
async def list_models(artifact_path: str=Depends(resolve_artifact_path)):
    return registry_client.list_model(artifact_path)