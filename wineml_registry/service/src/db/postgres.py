from db.base import BaseModelConnector


class PostgresModelConnector(BaseModelConnector):
    def __init__(
        self,
        username: str,
        password: str,
        host: str,
        port: str,
        database: str,
        connect_args: dict = {},
    ):
        engine_connector_string = (
            f"postgresql://{username}:{password}@{host}:{port}/{database}"
        )
        super().__init__(
            engine_connector_string,
            connect_args,
        )
