from fastapi import APIRouter

from ...registry import registry_client

router = APIRouter(tags=["user", "registry"])


@router.get("/artifact")
async def get_artifact(artifact_path: str):
    return registry_client.get_artifact(artifact_path)


@router.post("/artifact")
async def upload_artifact():
    registry_client.upload_artifact()
    return "OK", 200


@router.delete("/artifact")
async def delete_artifact():
    registry_client.delete_artifact()
    return "OK", 200
