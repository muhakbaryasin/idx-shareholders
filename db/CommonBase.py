from sqlalchemy import (
	Column,
    Integer,
    DateTime,
)

from sqlalchemy.sql import func
import datetime 

class CommonBase(object):
    @classmethod
    def common_action(self):
        self.id = Column(Integer, primary_key=True, autoincrement=True)
        self.created_by_id = Column(Integer, nullable=False)
        self.created_date = Column(DateTime(timezone=False), default=func.now(), nullable=False)
        self.modified_by_id = Column(Integer, nullable=True)
        self.modified_date = Column(DateTime(timezone=False), nullable=True)