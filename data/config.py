import os
import pathlib

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
DATABASE_DIR = pathlib.Path.cwd()

WEBHOOK_HOST = os.getenv('WEBHOOK_HOST')
WEBHOOK_PATH = f'/{BOT_TOKEN}'
WEBHOOK_URL = ''.join([WEBHOOK_HOST, WEBHOOK_PATH])

WEBAPP_HOST = os.getenv('WEBAPP_HOST')
WEBAPP_PORT = os.environ.get('PORT')

DATABASE_ENGINE = 'sqlite:///'
DATABASE_NAME = 'databasequiz.db'
DATABASE = os.path.join([DATABASE_ENGINE, DATABASE_DIR, DATABASE_NAME])
