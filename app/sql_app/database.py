from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+mysqldb://{}:{}@localhost/{}".format(
    "root", "Muvandi_10768", "jijenge"))
Session = sessionmaker()
Base = declarative_base()
