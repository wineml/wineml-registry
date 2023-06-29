import os

from constants import LOCAL_DB_PATH
from db.local import LocalModelConnector
from db.mysql import MysqlModelConnector
from db.postgres import PostgresModelConnector
from logger import logger


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
    elif all(
        [
            os.getenv("MYSQL_USER"),
            os.getenv("MYSQL_PASSWORD"),
            os.getenv("MYSQL_HOST"),
            os.getenv("MYSQL_PORT"),
            os.getenv("MYSQL_DATABASE"),
        ]
    ):
        return "mysql"
    else:
        return "local"


def initiate_db():
    """
    Initiate db based on db type
    """

    db_connector = db_resolver()
    logger.info(f"Connected to Database: {db_connector}")

    if db_connector == "postgres":
        return PostgresModelConnector(
            username=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            host=os.environ["POSTGRES_HOST"],
            port=os.environ["POSTGRES_PORT"],
            database=os.environ["POSTGRES_DB"],
        )
    elif db_connector == "mysql":
        return MysqlModelConnector(
            username=os.environ["MYSQL_USER"],
            password=os.environ["MYSQL_PASSWORD"],
            host=os.environ["MYSQL_HOST"],
            port=os.environ["MYSQL_PORT"],
            database=os.environ["MYSQL_DATABASE"],
        )
    elif db_connector == "local":
        return LocalModelConnector(os.getenv("LOCAL_DB_PATH", LOCAL_DB_PATH))
    else:
        raise ValueError("Invalid db_connector")


db_connector = initiate_db()
