from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data.config import DATABASE


engine = create_engine(DATABASE, echo=True)

Session = sessionmaker()
Session.configure(bind=engine)

session = Session()


# import os
# DATABASE_ENGINE = 'sqlite:///'
# DATABASE_DIR = pathlib.Path.cwd()
# DATABASE_NAME = 'databasequiz.db'
# DATABASE = ''.join([DATABASE_ENGINE, os.path.join(DATABASE_DIR, DATABASE_NAME)])
