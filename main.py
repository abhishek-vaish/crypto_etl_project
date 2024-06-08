from config import ARCHIVE_PATH, ETL_PATH, SNOWFLAKE_IDENTIFIER, SNOWFLAKE_USERNAME, \
    SNOWFLAKE_PASSWORD, API_KEY, COIN_RANKING_URI, COIN_RANKING_LIMIT, INTERNAL_STAGE
from src.etl.load import Load
from src.scrapping.scrap_cryptoranking import CryptoRanking

if __name__ == '__main__':
    # scrap data from coin ranking API
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
