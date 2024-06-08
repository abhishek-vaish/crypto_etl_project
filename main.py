from pathlib import Path
import os

from dotenv import load_dotenv

from src.scrapping.scrap_cryptoranking import CryptoRanking
from src.etl.load import Load


if __name__ == '__main__':
    BASE_PATH = Path(os.path.dirname(__file__))
    ARCHIVE_PATH = BASE_PATH / 'Data' / 'Archive'
    ETL_PATH = BASE_PATH / 'Data' / 'FilesForProcessing'
    load_dotenv(BASE_PATH / ".env")
    SNOWFLAKE_USERNAME = os.getenv("SNOWFLAKE_USERNAME")
    SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
    SNOWFLAKE_IDENTIFIER = os.getenv("SNOWFLAKE_IDENTIFIER")
    INTERNAL_STAGE = os.getenv("INTERNAL_STAGE")
    if not ETL_PATH.is_dir() or not ARCHIVE_PATH.is_dir():
        ETL_PATH.mkdir(exist_ok=True)
        ARCHIVE_PATH.mkdir(exist_ok=True)

    # scrap data from coin ranking API
    API_KEY = os.getenv("API_KEY")
    COIN_RANKING_URI = os.getenv("CRYPTO_RANKING_URI")
    COIN_RANKING_LIMIT = os.getenv("API_LIMIT")
    coinranking_obj = CryptoRanking(API_KEY,
                                    COIN_RANKING_URI,
                                    COIN_RANKING_LIMIT)
    coinranking_obj.req_crypto_ranking("currencies") \
        .save_to_json(ETL_PATH)

    # put file for snowflake internal stage
    Load(SNOWFLAKE_USERNAME,
         SNOWFLAKE_PASSWORD,
         SNOWFLAKE_IDENTIFIER,
         ETL_PATH,
         ARCHIVE_PATH,
         INTERNAL_STAGE) \
        .connect_engine() \
        .put_file() \
        .close()
