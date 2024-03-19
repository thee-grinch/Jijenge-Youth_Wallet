from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sql.models_alchemy import Base

sqlite_url = 'sqlite:///database.db'
engine = create_engine(sqlite_url, pool_size=10, pool_recycle=3600)


def create_db_and_tables():
    Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()