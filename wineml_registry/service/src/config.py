import os


class Environment:
    def __init__(self) -> None:
        self.env = os.getenv("ENVIRONMENT", "DEVELOPMENT")

    @property
    def is_production(self) -> bool:
        return self.env == "PRODUCTION"


class Config:
    ENVIRONMENT = Environment()
    SWAGGER_DOC_ROUTE = False if ENVIRONMENT.is_production else "/documentation"
