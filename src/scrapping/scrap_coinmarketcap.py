from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

from src.schema.schema_coinmarketcap import schema_coinmarketcap
from src.utilities.utility import convert_list_to_dict


class CoinMarketCap:
    def __init__(self):
        self.BASE_URL = "https://coinmarketcap.com/all/views/all/"
        self.coinmarketcap_lst = []

    def scrap_data(self):
        req = requests.get(self.BASE_URL)
        soup = BeautifulSoup(req.text, "lxml")
        crypto_table = \
            soup.find_all("div", {"class": "cmc-table__table-wrapper-outer"})[2]
        table_body = crypto_table.find("tbody")
        table_row = table_body.find_all("tr")
        for row in table_row:
            temp_coinmarketcap_lst = []
            table_data = row.find_all("td")
            for data in table_data:
                data_tag = data.find("div")
                if data_tag:
                    if data_tag.find("a"):
                        value = data_tag.find("a", {
                            "class": "cmc-table__column-name--name"}).text
                        temp_coinmarketcap_lst.append(value)
                    else:
                        temp_coinmarketcap_lst.append(data_tag.text)
                elif data.find("p"):
                    value = data.find("p").text
                    temp_coinmarketcap_lst.append(value)
                elif data.find("a"):
                    value = data.find("a").text
                    temp_coinmarketcap_lst.append(value)
            coinmarketcap_dict = convert_list_to_dict(temp_coinmarketcap_lst,
                                                      schema_coinmarketcap)
            self.coinmarketcap_lst.append(coinmarketcap_dict)
        return self.coinmarketcap_lst

    def convert_dict_to_csv(self, data_lst, target_path: Path):
        filename = 'coinmarketcap_' + datetime.strftime(datetime.now(), '%Y%m%d') \
                   + '_' + datetime.strftime(datetime.now(), '%H%M') + '.csv'
        df = pd.DataFrame(data_lst)
        df.dropna(inplace=True)
        df.to_csv(target_path / filename, index=False, sep=',', quotechar='"')
