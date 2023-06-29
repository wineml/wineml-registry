import os

from constants import LOCAL_DB_PATH


def db_resolver():
    """
    Check whether db is local or postgres (or mysql?)
    """

    if all(
        [
            os.getenv("POSTGRES_USER"),
            os.getenv("POSTGRES_PASSWORD"),
            os.getenv("POSTGRES_HOST"),
            os.getenv("POSTGRES_PORT"),
            os.getenv("POSTGRES_DB"),
        ]
    ):
        return "postgres"
    else:
        return "local"


def initiate_db():
    """
    Initiate db based on db type
    """

    db_connector = db_resolver()

    if db_connector == "postgres":
        from db.postgres import PostgresModelConnector

        return PostgresModelConnector(
            username=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            host=os.environ["POSTGRES_HOST"],
            port=os.environ["POSTGRES_PORT"],
            database=os.environ["POSTGRES_DB"],
        )
    elif db_connector == "mysql":
        ...
    elif db_connector == "local":
        from db.local import LocalModelConnector

        return LocalModelConnector(os.getenv("LOCAL_DB_PATH", LOCAL_DB_PATH))
    else:
        raise ValueError("Invalid db_connector")


db_connector = initiate_db()
