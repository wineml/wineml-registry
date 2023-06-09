from constants import VERSION
from fastapi import APIRouter

router = APIRouter()

####################################################################################################
# Generic APIs
####################################################################################################


@router.get("/health")
async def get_health():
    return "OK", 200


@router.get("/version")
async def get_version():
    return VERSION
