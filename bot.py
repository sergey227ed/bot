
from aiogram import Bot, Dispatcher, types, executor
import asyncio
import logging

API_TOKEN = '7229050941:AAGkTH895S0qBIDakK_0RAJCtoL6tNw_hzY'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

USERS_FILE = "users.txt"

def save_user(chat_id):
    try:
        with open(USERS_FILE, "a+") as f:
            f.seek(0)
            users = f.read().splitlines()
            if str(chat_id) not in users:
                f.write(f"{chat_id}\n")
    except:
        pass

def get_users():
    try:
        with open(USERS_FILE, "r") as f:
            return f.read().splitlines()
    except:
        return []

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    save_user(message.chat.id)
    await message.answer("✅ Вы подписались на рассылку.")

@dp.message_handler(commands=['sendall'])
async def sendall_cmd(message: types.Message):
    if str(message.from_user.id) != '7911493553':
        return await message.answer("🚫 У вас нет прав на рассылку.")

    text = message.text.replace("/sendall", "").strip()
    if not text:
        return await message.answer("Напишите текст рассылки после команды.")

    users = get_users()
    success, fail = 0, 0
    for user_id in users:
        try:
            await bot.send_message(user_id, text)
            success += 1
            await asyncio.sleep(0.1)
        except:
            fail += 1
    await message.answer(f"Рассылка завершена. ✅ Успешно: {success}, ❌ Ошибки: {fail}")
@dp.message_handler(commands=['audience'])
async def audience_cmd(message: types.Message):
    if str(message.from_user.id) != '7911493553':
        return
    users = get_users()
    await message.answer(f"👥 Аудитория: {len(users)} пользователей")
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
