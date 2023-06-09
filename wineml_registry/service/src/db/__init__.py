import os

from constants import LOCAL_DB_PATH


def db_resolver():
    """
    Check whether db is local or postgres (or mysql?)
    """

    if False:
        return "postgres"
    else:
        return "local"


def initiate_db():
    """
    Initiate db based on db type
    """

    db_connector = db_resolver()

    if db_connector == "postgres":
        ...
    elif db_connector == "mysql":
        ...
    elif db_connector == "local":
        from db.local import LocalModelConnector

        return LocalModelConnector(os.getenv("LOCAL_DB_PATH", LOCAL_DB_PATH))
    else:
        raise ValueError("Invalid db_connector")


db_connector = initiate_db()
