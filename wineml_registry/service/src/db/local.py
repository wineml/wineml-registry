from db.base import BaseModelConnector


class LocalModelConnector(BaseModelConnector):
    def __init__(
        self,
        engine_connector_string: str,
        connect_args: dict = {},
    ):
        super().__init__(
            engine_connector_string,
            connect_args,
        )
        self.local_db_path = engine_connector_string.split("///")[1]
