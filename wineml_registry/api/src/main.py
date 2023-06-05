from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import Config
from .constants import VERSION
from .routers import all_routers

app = FastAPI(
    title="WineML Registry Rest API",
    version=VERSION,
    docs_url=Config.SWAGGER_DOC_ROUTE,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


for router in all_routers:
    app.include_router(router)
