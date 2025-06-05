import os
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router

# Получаем токен и настройки вебхука из переменных окружения
TOKEN = os.getenv("TOKEN")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "supersecret")
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST", "https://your-app-url.onrender.com")
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# Создаем бота и диспетчер
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Роутер
router = Router()
dp.include_router(router)

@router.message()
async def start_handler(message: types.Message):
    if message.text == "/start":
        await message.answer("👋 Бот запущен через Webhook!")

# Настройка и запуск приложения
async def on_startup(bot: Bot):
    await bot.set_webhook(WEBHOOK_URL, secret_token=WEBHOOK_SECRET)

app = web.Application()
SimpleRequestHandler(dispatcher=dp, bot=bot, secret_token=WEBHOOK_SECRET).register(app, path=WEBHOOK_PATH)
setup_application(app, dp, bot=bot, on_startup=on_startup)


    
