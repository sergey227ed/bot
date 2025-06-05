import os
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

# Логирование
logging.basicConfig(level=logging.INFO)

# Переменные окружения
TOKEN = os.getenv("TOKEN")
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST")  # Например: https://bot-abc123.onrender.com
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# Создание бота и диспетчера
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

# Обработчик команды /start
@dp.message(commands=["start"])
async def start_handler(message: Message):
    await message.answer("Привет! Бот работает через webhook 🎉")

# Приложение aiohttp
async def on_startup(app: web.Application):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(app: web.Application):
    await bot.delete_webhook()

app = web.Application()
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
setup_application(app, dp)

if name == "main":
    web.run_app(app, host="0.0.0.0", port=int(os.getenv("PORT", 1000)))
