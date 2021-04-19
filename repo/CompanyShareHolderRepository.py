from sqlalchemy import inspect
from sqlalchemy.orm.collections import InstrumentedList
from db.session_manager import session_manager
from db.Company import Company
from db.ShareHolder import ShareHolder
from db.CompanyShareHolder import CompanyShareHolder
from datetime import datetime


class CompanyShareHolderRepository(object):
	def __dict_to_companyshareholder__(self, entity):
		return CompanyShareHolder(**entity)
	
	def add(self, entity):
		with session_manager() as session:
			entry = self.__dict_to_companyshareholder__(entity)
			entry.create_date = datetime.now()
			session.add(entry)
			session.commit()
			session.refresh(entry)
		return entry


	def update(self, entry_update):
		if type(entry_update) is dict:
			entry_update.pop('update_date', None)
			entry_update = CompanyShareHolder(**entry_update)
		
		entry_update.update_date = datetime.now()
		
		with session_manager() as session:
			entry = session.query(CompanyShareHolder).filter(CompanyShareHolder.id==entry_update.id).one_or_none() 
			
			if entry is None:
				return
			
			mapper = inspect(entry)
			
			for column in mapper.attrs:
				if type(entry.__getattribute__( column.key )) is InstrumentedList:
					continue
				if type(entry.__getattribute__( column.key )) is Company:
					continue
				if type(entry.__getattribute__( column.key )) is ShareHolder:
					continue
				
				setattr(entry, column.key, entry_update.__getattribute__( column.key ))
			
			session.commit()
			session.refresh(entry)
			
		return entry


	def get(self, id):
		import pdb; pdb.set_trace()
		with session_manager() as session:
			return session.query(CompanyShareHolder).filter(CompanyShareHolder.id==id).one_or_none()
	
	def get(self, company_id, shareholder_id):
		with session_manager() as session:
			return session.query(CompanyShareHolder).filter(CompanyShareHolder.company_id==company_id).filter(CompanyShareHolder.shareholder_id==shareholder_id).one_or_none()
	
	def get_by_shareholder_id(self, shareholder_id):
		with session_manager() as session:
			return session.query(CompanyShareHolder).filter(CompanyShareHolder.shareholder_id==shareholder_id).all()
	
	def delete(self, id):
		entry = self.get(id)
		
		with session_manager() as session:
			session.delete(entry)
			session.commit()
		
		return entry
