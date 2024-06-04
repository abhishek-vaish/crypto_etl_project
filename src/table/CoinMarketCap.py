from datetime import datetime

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime


Base = declarative_base()


class BaseCoinMarketCap(Base):
    __tablename__ = "CoinMarketCap"
    __table_args__ = {
        "schema": "raw"
    }
    Id = Column(Integer, primary_key=True)
    Rank = Column(Integer, name="RANK")
    Name = Column(String, name="NAME")
    Symbol = Column(String, name="SYMBOL")
    Type = Column(String, name="TYPE")
    Category = Column(String, name="CATEGORY")
    Image = Column(String, name="IMAGE")
    MarketCap = Column(String, name="MARKETCAP")
    Price = Column(String, name="PRICE")
    CirculatingSupply = Column(String, name="CIRCULATINGSUPPLY")
    TotalSupply = Column(String, name="TOTALSUPPLY")
    MaxSupply = Column(String, name="MAXSUPPLY")
    Volume = Column(String, name="VOLUME")
    PercentChangeSixMin = Column(String, name="PERCENTCHANGESIXMIN")
    PercentChangeWeek = Column(String, name="PERCENTCHANGEWEEK")
    PercentChangeDay = Column(String, name="PERCENTCHANGEDAY")
    PercentChangeMonth = Column(String, name="PERCENTCHANGEMONTH")
    DayHigh = Column(String, name="DAYHIGH")
    DayLow = Column(String, name="DAYLOW")
    LastUpdated = Column(DateTime, name="LASTUPDATED")
    FileDate = Column(DateTime, name="FILEDATE")
    CreatedAt = Column(DateTime, default=datetime.now(), name="CREATEDAT")

    def __init__(self, engine):
        Base.metadata.create_all(engine)

