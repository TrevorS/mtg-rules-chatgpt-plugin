from sqlalchemy import Column, Float, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from . import config

engine = create_engine(
    f"sqlite:///{config.get_cards_db_path()}",
    connect_args={
        "check_same_thread": False,
    },
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


class BaseType(Base):
    __abstract__ = True


class Card(BaseType):
    __tablename__ = "cards"
    artist = Column(String, nullable=True)
    colors = Column(String, nullable=True)
    keywords = Column(String, nullable=True)
    loyalty = Column(String, nullable=True)
    manaCost = Column(String, nullable=True)
    manaValue = Column(Float, nullable=True)
    name = Column(String(collation="NOCASE"), nullable=True)
    power = Column(String, nullable=True)
    scryfallId = Column(String, nullable=True)
    setCode = Column(String, nullable=True)
    text = Column(String, nullable=True)
    toughness = Column(String, nullable=True)
    types = Column(String, nullable=True)
    uuid = Column(String, primary_key=True)
