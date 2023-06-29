import uvicorn
from config import Config
from constants import VERSION
from db import db_connector
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import all_routers

# main app
app = FastAPI(
    title="WineML Registry Service",
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


@app.on_event("startup")
async def startup_event():
    db_connector.create_all_tables()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8081, reload=True, log_level="debug")
