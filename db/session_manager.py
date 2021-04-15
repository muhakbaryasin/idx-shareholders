from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from contextlib import contextmanager
import configparser
from pathlib import Path


def get_db_config_url():
    file_path = 'db_config.ini'
    db_config_file = Path(file_path)

    config = configparser.ConfigParser()
    
    config['CONNECTION'] = {}
    config['CONNECTION']['url'] = ''

    if not db_config_file.is_file():
        with open(file_path, 'w') as configfile:    # save
            config.write(configfile)
        
    config.read(file_path)

    return config['CONNECTION']['url']
    

@contextmanager
def session_manager():
    """provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
    except:
        session.rollback()
        raise
    finally:
        session.close()


engine = create_engine(get_db_config_url(), connect_args={'connect_timeout': 1000}, pool_size=20, pool_pre_ping=True, pool_recycle=3600)
# engine = create_engine('postgres://hypothesis-h-prod-db.us-west-1.rds.amazonaws.com:5432/h?keepalives_idle=60&keepalives_interval=60&keepalives_count=10', pool_size=5, max_overflow=2, timeout=30, use_lifo=False)
Session = sessionmaker(bind=engine)