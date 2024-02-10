from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

sqlite_url = 'sqlite:///database.db'
engine = create_engine(sqlite_url, pool_size=10, pool_recycle=3600)

def create_db_and_tables():
    Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()