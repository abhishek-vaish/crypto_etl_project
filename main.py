from config import ARCHIVE_PATH, ETL_PATH, SNOWFLAKE_IDENTIFIER, SNOWFLAKE_USERNAME, \
    SNOWFLAKE_PASSWORD, API_KEY, COIN_RANKING_URI, COIN_RANKING_LIMIT, INTERNAL_STAGE, \
    INTERNAL_ARCHIVE_STAGE, INTERNAL_STAGE_FILE_PATTERN
from src.etl.load import Load
from src.scrapping.scrap_cryptoranking import CryptoRanking
from src.utilities.logger import logger

if __name__ == '__main__':
    # scrap data from coin ranking API
    logger.info("Fetching Coin Ranking Data from API")
    coinranking_obj = CryptoRanking(API_KEY,
                                    COIN_RANKING_URI,
                                    COIN_RANKING_LIMIT)
    logger.info("Data fetch successfully from the API")
    logger.info(f"Saving data into JSON file at {ETL_PATH}")
    coinranking_obj.req_crypto_ranking("currencies") \
        .save_to_json(ETL_PATH)
    logger.info("File save successfully at expected ETL path")

    # put file for snowflake internal stage
    logger.info("Uploading file to Snowflake Internal Stage")
    Load(SNOWFLAKE_USERNAME,
         SNOWFLAKE_PASSWORD,
         SNOWFLAKE_IDENTIFIER,
         ETL_PATH,
         ARCHIVE_PATH,
         INTERNAL_STAGE,
         INTERNAL_ARCHIVE_STAGE,
         INTERNAL_STAGE_FILE_PATTERN) \
        .connect_engine() \
        .put_file() \
        .close()
    logger.info("File successfully uploaded to Snowflake internal stage")
