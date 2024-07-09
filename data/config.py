import os
import pathlib

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

WEBHOOK_HOST = os.getenv('WEBHOOK_HOST')
WEBHOOK_PATH = f'/{BOT_TOKEN}'
WEBHOOK_URL = ''.join([WEBHOOK_HOST, WEBHOOK_PATH])

WEBAPP_HOST = os.getenv('WEBAPP_HOST')
WEBAPP_PORT = os.getenv('WEBAPP_PORT')

DB_DIR = pathlib.Path.cwd()
DB_ENGINE = 'sqlite:///'
DB_NAME = f"{os.getenv('DB_NAME', 'databasequiz')}.db"
DB_URI = os.path.join(DB_ENGINE, DB_DIR, DB_NAME)
