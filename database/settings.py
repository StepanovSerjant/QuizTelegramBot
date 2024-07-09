from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data.config import DB_URI

engine = create_engine(DB_URI, echo=True)

Session = sessionmaker()
Session.configure(bind=engine)

session = Session()
