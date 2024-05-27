from pathlib import Path
from datetime import datetime
import os

from dotenv import load_dotenv

from src.scrapping.scrap_coinmarketcap import CoinMarketCap
from src.etl.transformation import Transformation
from src.etl.load import Load
from src.table.CoinMarketCap import BaseCoinMarketCap
from src.utilities.utility import archive_file


if __name__ == '__main__':
    BASE_PATH = Path(os.path.dirname(__file__))
    ARCHIVE_PATH = BASE_PATH / 'Data' / 'Archive'
    ETL_PATH = BASE_PATH / 'Data' / 'FilesForProcessing'
    load_dotenv(BASE_PATH / ".env")
    SERVER_NAME = os.getenv("DATABASE_SERVER")
    if not ETL_PATH.is_dir() or not ARCHIVE_PATH.is_dir():
        ETL_PATH.mkdir(exist_ok=True)
        ARCHIVE_PATH.mkdir(exist_ok=True)

    # scrap data from the target link
    coinmarketcap_obj = CoinMarketCap()
    coinmarketcap_lst = coinmarketcap_obj.scrap_data()
    coinmarketcap_obj.convert_dict_to_csv(coinmarketcap_lst, ETL_PATH)

    # process files
    for file in ETL_PATH.glob("coinmarketcap_*.csv"):
        if file:
            # create file date
            file_datetime = str(file).split("_")[1] + " " + str(file).split("_")[2][:-4]
            file_datetime = datetime.strptime(file_datetime, '%Y%m%d %H%M')

            # perform transformation
            transformation = Transformation(file_path=file) \
                .file_format("csv") \
                .read_file() \
                .remove_null() \
                .remove_duplicate() \
                .split_substring("market_cap", "\\$[0-9]+\\.[0-9]+[A-Z]") \
                .cast("rank", int) \
                .generate_dict()

            # load data to sql table
            Load(transformation, SERVER_NAME) \
                .connect_engine() \
                .get_key("coinmarketcap", "raw")\
                .insert(BaseCoinMarketCap, file_datetime) \
                .close()

            # archive process files
            file_string = os.path.split(file)[1]
            arhive_file_path = ARCHIVE_PATH / file_string
            archive_file(file, arhive_file_path)
        else:
            raise FileNotFoundError(f"No files found at: {ETL_PATH}")

