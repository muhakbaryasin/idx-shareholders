from sqlalchemy import inspect
from sqlalchemy.orm.collections import InstrumentedList
from db.session_manager import session_manager
from db.Company import Company
from datetime import datetime

class CompanyRepository(object):
	def __dict_to_company__(self, entity):
		return Company(**entity)
	
	def add(self, entity):
		with session_manager() as session:
			entry = self.__dict_to_company__(entity)
			session.add(entry)
			session.commit()
			session.refresh(entry)
		return entry


	def update(self, entry_update):
		if type(entry_update) is dict:
			entry_update.pop('update_date', None)
			entry_update = Company(**entry_update)
		
		entry_update.update_date = datetime.now()
		
		with session_manager() as session:
			entry = session.query(Company).filter(Company.id==entry_update.id).one_or_none() 
			
			if entry is None:
				return
			
			mapper = inspect(entry)
			
			for column in mapper.attrs:
				if type(entry.__getattribute__( column.key )) is InstrumentedList:
					continue
					
				setattr(entry, column.key, entry_update.__getattribute__( column.key ))
			
			session.commit()
			session.refresh(entry)
			
		return entry


	def get(self, id):
		with session_manager() as session:
			return session.query(Company).filter(Company.id==id).one_or_none()
    
	def get_by_code(self, code):
		with session_manager() as session:
			return session.query(Company).filter(Company.code==code).one_or_none()
    

	def delete(self, id):
		entry = self.get(id)
		
		with session_manager() as session:
			session.delete(entry)
			session.commit()
		
		return entry
