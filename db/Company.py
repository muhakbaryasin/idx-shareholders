from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Text,
    TIMESTAMP,
)

from db.meta import BaseEntity, Base
from sqlalchemy.sql import func


class Company(Base):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    code = Column(Text, nullable=False)
    listing_date = Column(DateTime, nullable=False)
    create_date = Column(TIMESTAMP, default=func.now(), nullable=False)
    update_date = Column(TIMESTAMP, default=func.now(), nullable=False)
