import logging
import os

from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

# === Конфигурация ===
TOKEN = os.getenv("TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_HOST = "https://bot-xxxxx.onrender.com"  # <-- ВСТАВЬ СЮДА СВОЙ URL из Render
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# === Бот и диспетчер ===
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

# === Хендлер команды /start ===
@dp.message(F.text == "/start")
async def cmd_start(message: types.Message):
    await message.answer("Привет! Бот на webhook работает!")

# === Webhook сервер ===
async def on_startup(bot: Bot):
    await bot.set_webhook(WEBHOOK_URL)

app = web.Application()
SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
app.on_startup.append(lambda _: on_startup(bot))
setup_application(app, dp, bot=bot)

# === Для Render просто оставь как есть, он сам запустит app ===
