from sqlalchemy.engine import create_engine
from sqlalchemy import text
from urllib import parse

from src.utilities.utility import archive_file
from src.utilities.logger import logger


class Load:
    def __init__(self, snowflake_username,
                 snowflake_password,
                 snowflake_identifier,
                 etl_path,
                 archive_path,
                 internal_stage,
                 internal_archive_stage,
                 internal_stage_file_pattern):
        self.username = snowflake_username
        self.password = snowflake_password
        self.identifier = snowflake_identifier
        self.etl_path = etl_path
        self.archive_path = archive_path
        self.internal_stage = internal_stage
        self.internal_archive_stage = internal_archive_stage
        self.internal_stage_file_pattern = internal_stage_file_pattern
        self.cursor = None

    def connect_engine(self):
        snowflake_uri = f"snowflake://{self.username}:{self.password}@{parse.quote(self.identifier)}/WH_CRYPTO"
        engine = create_engine(url=snowflake_uri, echo=True)
        try:
            self.cursor = engine.connect()
            logger.info("Snowflake connected successfully")
            return self
        except ConnectionError:
            logger.error("Unable to connect with database")

    def put_file(self):
        file_lst = self.etl_path.glob("cryptoranking_*.json")
        if file_lst is not None:
            for file_path in file_lst:
                file_path = str(file_path).replace("\\", "/")
                copy_query = text(f'COPY FILES INTO '
                                  f'{self.internal_archive_stage} '
                                  f'FROM {self.internal_stage} '
                                  f'PATTERN="{self.internal_stage_file_pattern}"')
                remove_query = text(f'REMOVE {self.internal_stage} '
                                    f'PATTERN="{self.internal_stage_file_pattern}"')
                logger.info("Copy files from processing stage to archive stage")
                self.cursor.execute(copy_query)

                logger.info("Removing files from processing stage")
                self.cursor.execute(remove_query)

                query = text(f"PUT file://{file_path} {self.internal_stage}")
                self.cursor.execute(query)

                logger.info("Archiving processed file")
                archive_file(file_path, self.archive_path)
                logger.info("File successfully archived")
        return self

    def close(self):
        logger.info("Closing Snowflake connection")
        self.cursor.close()


