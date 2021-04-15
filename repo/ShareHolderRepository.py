from sqlalchemy import inspect
from sqlalchemy.orm.collections import InstrumentedList
from db.session_manager import session_manager
from db.ShareHolder import ShareHolder
from db.Company import Company
from datetime import datetime


class ShareHolderRepository(object):
	def __dict_to_shareholder__(self, entity):
		return ShareHolder(**entity)
	
	def add(self, entity):
		with session_manager() as session:
			entry = self.__dict_to_shareholder__(entity)
			session.add(entry)
			session.commit()
			session.refresh(entry)
		return entry


	def update(self, entry_update):
		if type(entry_update) is dict:
			entry_update.pop('update_date', None)
			entry_update = ShareHolder(**entry_update)
		
		entry_update.update_date = datetime.now()
		
		with session_manager() as session:
			entry = session.query(ShareHolder).filter(ShareHolder.id==entry_update.id).one_or_none() 
			
			if entry is None:
				return
			
			mapper = inspect(entry)
			
			for column in mapper.attrs:
				if type(entry.__getattribute__( column.key )) is InstrumentedList:
					continue
				if type(entry.__getattribute__( column.key )) is Company:
					continue
				
				setattr(entry, column.key, entry_update.__getattribute__( column.key ))
			
			session.commit()
			session.refresh(entry)
			
		return entry


	def get(self, id):
		with session_manager() as session:
			return session.query(ShareHolder).filter(ShareHolder.id==id).one_or_none()
	
	def get_by_name(self, company_id, name):
		with session_manager() as session:
			return session.query(ShareHolder).filter(ShareHolder.company_id==company_id and ShareHolder.name==name).one_or_none()
	
	def get_paginate(self, page=0, page_size=10):
		with session_manager() as session:
			query = session.query(Company, ShareHolder).join(ShareHolder, ShareHolder.company_id==Company.id).order_by(ShareHolder.share.desc())
			
			if page_size:
				query = query.limit(page_size)
			if page: 
				query = query.offset(page*page_size)
			
			return query.all()
    
	def delete(self, id):
		entry = self.get(id)
		
		with session_manager() as session:
			session.delete(entry)
			session.commit()
		
		return entry
