from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    BigInteger,
    String,
)

from db.meta import Base
from sqlalchemy.sql import func


class Company(Base):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), index=True, unique=True, nullable=False,)
    code = Column(String(4), index=True, unique=True, nullable=False,)
    listing_date = Column(DateTime(timezone=False), nullable=False)
    market_capitalization = Column(BigInteger, nullable=False)
    create_date = Column(DateTime, default=func.now(), nullable=False)
    update_date = Column(DateTime, default=func.now(), nullable=False)
