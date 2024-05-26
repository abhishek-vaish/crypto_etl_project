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
    Rank = Column(Integer)
    Name = Column(String)
    Symbol = Column(String)
    MarketCap = Column(String)
    Price = Column(String)
    CirculatingSupply = Column(String)
    Volume = Column(String)
    PercentPerHour = Column(String)
    PercentPerWeek = Column(String)
    PercentPerDay = Column(String)
    FileDate = Column(DateTime)
    CreatedAt = Column(DateTime, default=datetime.now())

    def __init__(self, engine):
        Base.metadata.create_all(engine)

