from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
    BigInteger,
    ForeignKey
)

from db.meta import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class CompanyShareHolder(Base):
    __tablename__ = 'company_shareholder'
    id = Column(Integer, primary_key=True)
    shareholder_id = Column(Integer, ForeignKey('shareholder.id'))
    shareholder = relationship('ShareHolder', backref='company_shareholder_shareholder')
    company_id = Column(Integer, ForeignKey('company.id'))
    company = relationship('Company', backref='company_shareholder_company')
    share = Column(BigInteger, nullable=False)
    create_date = Column(DateTime, default=func.now(), nullable=False)
    update_date = Column(DateTime, default=func.now(), nullable=False)
