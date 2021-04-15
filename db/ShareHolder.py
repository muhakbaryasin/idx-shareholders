from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Text,
    BigInteger,
    ForeignKey
)

from db.meta import BaseEntity, Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class ShareHolder(Base):
    __tablename__ = 'shareholder'
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('company.id'))
    company = relationship('Company', backref='shareholder_company')
    name = Column(Text, nullable=False)
    share = Column(BigInteger, nullable=False)
    create_date = Column(DateTime, default=func.now(), nullable=False)
    update_date = Column(DateTime, default=func.now(), nullable=False)
