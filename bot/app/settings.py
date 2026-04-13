import os

from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
BACKEND_API_URL = os.environ["BACKEND_API_URL"]
BOT_API_TOKEN = os.environ["BOT_API_TOKEN"]
