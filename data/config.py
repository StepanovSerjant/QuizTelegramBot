import os
import pathlib

from dotenv import load_dotenv


load_dotenv()
BOT_TOKEN = str(os.getenv('BOT_TOKEN'))

WEBHOOK_HOST = str(os.getenv('WEBHOOK_HOST'))
WEBHOOK_PATH = str(os.getenv('WEBHOOK_PATH'))
WEBHOOK_URL = ''.join([WEBHOOK_HOST, WEBHOOK_PATH])

WEBAPP_HOST = str(os.getenv('WEBAPP_HOST'))
WEBAPP_PORT = os.environ.get('PORT')

DATABASE_ENGINE = 'sqlite:///'
DATABASE_DIR = pathlib.Path.cwd()
DATABASE_NAME = 'databasequiz.db'
DATABASE = ''.join([DATABASE_ENGINE, os.path.join(DATABASE_DIR, DATABASE_NAME)])
