import config
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
    Load(config.SNOWFLAKE_USERNAME,
         config.SNOWFLAKE_PASSWORD,
         config.SNOWFLAKE_IDENTIFIER,
         config.ETL_PATH,
         config.ARCHIVE_PATH,
         config.INTERNAL_STAGE,
         config.INTERNAL_ARCHIVE_STAGE,
         config.INTERNAL_STAGE_FILE_PATTERN) \
        .connect_engine() \
        .put_file() \
        .close()
    logger.info("File successfully uploaded to Snowflake internal stage")
