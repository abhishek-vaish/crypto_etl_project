import requests
from datetime import datetime
from pathlib import Path
from urllib import parse


class CryptoRanking:
    def __init__(self, api_key, uri, limit):
        self._api_key = api_key
        self._uri = uri
        self._limit = limit
        self._response = None

    def req_crypto_ranking(self, endpoints):
        params = {
            "api_key": self._api_key,
            "limit": self._limit,
            "optionalFields": "images"
        }
        uri = parse.urljoin(self._uri, endpoints)
        print(uri)
        res = requests.get(uri, params)
        self._response = res.text
        return self

    def save_to_json(self, target_path: Path):
        current_date = datetime.strftime(datetime.now(), '%Y%m%d')
        filename = f"cryptoranking_{current_date}.json"
        file_path = target_path / filename
        if not file_path.exists():
            with open(file_path, 'w', encoding="utf-8") as file:
                file.write(self._response)
        else:
            raise FileExistsError(f"{filename} already exists.")
        return self


