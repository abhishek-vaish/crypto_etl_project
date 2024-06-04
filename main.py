from pathlib import Path
import os

from dotenv import load_dotenv

from src.scrapping.scrap_cryptoranking import CryptoRanking
from src.etl.extract_coinranking import ExtractCoinRanking
from src.etl.load import Load
from src.table.CoinRanking import BaseCoinMarketCap


if __name__ == '__main__':
    BASE_PATH = Path(os.path.dirname(__file__))
    ARCHIVE_PATH = BASE_PATH / 'Data' / 'Archive'
    ETL_PATH = BASE_PATH / 'Data' / 'FilesForProcessing'
    load_dotenv(BASE_PATH / ".env")
    SERVER_NAME = os.getenv("DATABASE_SERVER")
    if not ETL_PATH.is_dir() or not ARCHIVE_PATH.is_dir():
        ETL_PATH.mkdir(exist_ok=True)
        ARCHIVE_PATH.mkdir(exist_ok=True)

    # scrap data from coin ranking API
    API_KEY = os.getenv("API_KEY")
    COIN_RANKING_URI = os.getenv("CRYPTO_RANKING_URI")
    COIN_RANKING_LIMIT = os.getenv("API_LIMIT")
    COIN_RANKING_VERSION = os.getenv("CRYPTO_RANKING_VERSION")
    coinranking_obj = CryptoRanking(API_KEY,
                                    COIN_RANKING_URI,
                                    COIN_RANKING_LIMIT)
    coinranking_obj.req_crypto_ranking("currencies") \
        .save_to_json(ETL_PATH)

    data_list = ExtractCoinRanking(ETL_PATH) \
        .format("json") \
        .read_file("cryptoranking_*") \
        .get_dictonary()

    Load(data_list, SERVER_NAME) \
        .connect_engine() \
        .insert(BaseCoinMarketCap) \
        .close()
