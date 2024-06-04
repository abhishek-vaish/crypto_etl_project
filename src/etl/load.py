from sqlalchemy.engine import create_engine
from sqlalchemy import text


class Load:
    def __init__(self, data_dict: list, server_name):
        self.df = data_dict
        self.db_server = server_name
        self.cursor = None
        self.key = 0

    def connect_engine(self):
        engine = create_engine(url=self.db_server, echo=True)
        try:
            self.cursor = engine.connect()
            return self
        except ConnectionError:
            raise ConnectionError("Unable to connect with database")

    def get_key(self, tablename, schema):
        query = f"select max(id) from {schema}.{tablename}"
        key = self.cursor.execute(text(query)).fetchone()[0]
        self.key = key if key is not None else 0
        return self

    def insert(self, table_name):
        for row in self.df:
            self.cursor.execute(table_name.__table__.insert().values(row))
            self.cursor.commit()
        return self

    def close(self):
        self.cursor.close()


