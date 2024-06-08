from pathlib import Path
from datetime import datetime
import json
import os

from src.utilities.utility import archive_file


class ExtractCoinRanking:
    def __init__(self, etl_path: Path):
        self.etl_path = etl_path
        self.type = None
        self.dataframe = None
        self.data_list = []
        self.file_date = None

    def format(self, format_type):
        self.type = format_type
        return self

    def read_file(self, file_pattern, archive_path):
        for file in self.etl_path.glob(file_pattern):
            if file:
                self.file_date = datetime.strptime(file.name.split("_")[1][:-5]
                                                   , "%Y%m%d")
                if self.type == "json":
                    with open(file, 'r') as rfile:
                        self.dataframe = json.loads(rfile.readline())
                    file_string = os.path.split(file)[1]
                    archive_file_path = archive_path / file_string
                    archive_file(file, archive_file_path)
            else:
                raise FileNotFoundError(f"No files found at: {self.etl_path}")
        return self

    def get_dictonary(self):
        if self.dataframe is not None:
            for data in self.dataframe["data"]:
                self.data_list.append({
                    "RANK": data["rank"],
                    "NAME": data["name"],
                    "SYMBOL": data["symbol"],
                    "TYPE": data["type"],
                    "CATEGORY": data.setdefault("category", None),
                    "IMAGE": data["images"]["60x60"],
                    "MARKETCAP": data["values"]["USD"]["marketCap"],
                    "PRICE": data["values"]["USD"]["price"],
                    "CIRCULATINGSUPPLY": data["circulatingSupply"],
                    "TOTALSUPPLY": data.setdefault("totalSupply", None),
                    "MAXSUPPLY": data.setdefault("maxSupply", None),
                    "VOLUME": data["values"]["USD"]["volume24h"],
                    "PERCENTCHANGESIXMIN": data["values"]["USD"]["percentChange6m"],
                    "PERCENTCHANGEWEEK": data["values"]["USD"]["percentChange7d"],
                    "PERCENTCHANGEDAY": data["values"]["USD"]["percentChange24h"],
                    "PERCENTCHANGEMONTH": data["values"]["USD"]["percentChange30d"],
                    "DAYHIGH": data["values"]["USD"]["high24h"],
                    "DAYLOW": data["values"]["USD"]["low24h"],
                    "LASTUPDATED": data["lastUpdated"],
                    "FILEDATE": self.file_date
                })
        return self.data_list
