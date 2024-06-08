from sqlalchemy.engine import create_engine
from sqlalchemy import text
from urllib import parse

from src.utilities.utility import archive_file


class Load:
    def __init__(self, snowflake_username,
                 snowflake_password,
                 snowflake_identifier,
                 etl_path,
                 archive_path,
                 internal_stage):
        self.username = snowflake_username
        self.password = snowflake_password
        self.identifier = snowflake_identifier
        self.etl_path = etl_path
        self.archive_path = archive_path
        self.internal_stage = internal_stage
        self.cursor = None

    def connect_engine(self):
        snowflake_uri = f"snowflake://{self.username}:{self.password}@{parse.quote(self.identifier)}/WH_CRYPTO"
        engine = create_engine(url=snowflake_uri, echo=True)
        try:
            self.cursor = engine.connect()
            return self
        except ConnectionError:
            raise ConnectionError("Unable to connect with database")

    def put_file(self):
        for file_path in self.etl_path.glob("cryptoranking_*.json"):
            file_path = str(file_path).replace("\\", "/")
            query = text(f"PUT file://{file_path} {self.internal_stage}")
            print(query)
            self.cursor.execute(query)
            archive_file(file_path, self.archive_path)
        return self

    def close(self):
        self.cursor.close()


