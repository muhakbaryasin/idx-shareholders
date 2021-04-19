from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
    BigInteger,
)

from db.meta import Base
from sqlalchemy.sql import func


class ShareHolder(Base):
    __tablename__ = 'shareholder'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), index=True, unique=True, nullable=False)
    share = Column(BigInteger, nullable=False)
    create_date = Column(DateTime, default=func.now(), nullable=False)
    update_date = Column(DateTime, default=func.now(), nullable=False)
