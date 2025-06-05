import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

# Настройки
TOKEN = os.getenv("TOKEN")
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST", "https://твой-проект.onrender.com")  # Замени на свой
WEBHOOK_PATH = "/webhook"
WEBHOOK_SECRET = "supersecret"  # Любая строка
WEBHOOK_URL = WEBHOOK_HOST + WEBHOOK_PATH

# Бот и диспетчер
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

# Хендлер
@dp.message(commands=["/start"])
async def cmd_start(message: types.Message):
    await message.answer("🤖 Бот работает через webhook!")

# Настройки webhook
async def on_startup(app: web.Application):
    await bot.set_webhook(WEBHOOK_URL, secret_token=WEBHOOK_SECRET)
    print("✅ Webhook установлен")

async def on_shutdown(app: web.Application):
    await bot.delete_webhook()
    print("❌ Webhook удалён")

# Запуск
async def main():
    app = web.Application()
    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET
    ).register(app, path=WEBHOOK_PATH)


    
