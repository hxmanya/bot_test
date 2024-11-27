from aiogram import Bot, Dispatcher, types
from dotenv import dotenv_values

from database.database import Database

database = Database("database.sqlite")

token = dotenv_values(".env")["BOT_TOKEN"]
bot = Bot(token=token)
dp = Dispatcher()
groups = ['Python 47-01', 'Python 47-02', 'Python 48-01', 'Python 48-02']
