from sqlalchemy import inspect
from sqlalchemy.orm.collections import InstrumentedList
from db.session_manager import session_manager
from db.Company import Company


class CompanyRepository(object):
    def add(self, entity):
        with session_manager() as session:
            entry = Company(**entity)
            session.add(entry)
            session.commit()
            session.refresh(entry)
        return entry


    def update(self, entry_update):
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
        return entry


    def get(self, id):
        with session_manager() as session:
            return session.query(Company).filter(Company.id==id).one_or_none()
    

    def delete(self, id):
        entry = self.get(id)
        
        with session_manager() as session:
            session.delete(entry)
            session.commit()
        
        return entry
