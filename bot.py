import logging
import os

from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

# === Настройки ===
TOKEN = os.getenv("TOKEN")
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST", "https://bot-303u.onrender.com")  # замени на свой Render-домен
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
ADMIN_ID = 7911493553  # ← твой ID

# === Бот и диспетчер ===
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

# === Команда /start ===
@dp.message(F.text == "/start")
async def cmd_start(message: types.Message):
    user_id = str(message.from_user.id)
    if not os.path.exists("users.txt"):
        open("users.txt", "w").close()

    with open("users.txt", "r", encoding="utf-8") as file:
        users = file.read().splitlines()

    if user_id not in users:
        with open("users.txt", "a", encoding="utf-8") as file:
            file.write(user_id + "\n")

    await message.answer("✅ Бот работает на webhook!")

# === Команда /send — Рассылка ===
@dp.message(F.text.startswith("/send"))
async def broadcast(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔️ У тебя нет доступа к этой команде.")
        return

    text_to_send = message.text[6:].strip()
    if not text_to_send:
        await message.answer("❗️ Напиши текст после /send.")
        return

    if not os.path.exists("users.txt"):
        await message.answer("❗️ Файл users.txt не найден.")
        return

    with open("users.txt", "r", encoding="utf-8") as file:
        users = [line.strip() for line in file if line.strip().isdigit()]

    success, fail = 0, 0
    valid_users = []

    for user_id in users:
        try:
            await bot.send_message(chat_id=int(user_id), text=text_to_send)
            valid_users.append(user_id)
            success += 1
        except Exception as e:
            fail += 1
            logging.error(f"❌ Не удалось отправить сообщение {user_id}: {e}")

    # Перезапись файла только с рабочими ID
    with open("users.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(valid_users))

    await message.answer(f"✅ Рассылка завершена!\n\nУспешно: {success}\nОшибок: {fail}")

# === Webhook ===
async def on_startup(bot: Bot):
    await bot.set_webhook(WEBHOOK_URL)

app = web.Application()
SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
app.on_startup.append(lambda _: on_startup(bot))
setup_application(app, dp, bot=bot)

# === Запуск на Render ===
if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
        
