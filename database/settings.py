from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data.config import DATABASE


engine = create_engine(DATABASE, echo=True)

Session = sessionmaker()
Session.configure(bind=engine)

session = Session()
