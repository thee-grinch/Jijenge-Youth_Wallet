from sqlmodel import SQLModel, create_engine
from sqlmodel import Session


sqlite_url = 'sqlite:///database.db'
engine = create_engine(sqlite_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()