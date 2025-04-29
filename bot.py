from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import pytz
import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 805696670

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        ["🏠 Хочу купить", "🏘️ Хочу продать"],
        ["ℹ️ Обо мне"]
    ],
    resize_keyboard=True
)

buy_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        ["🏢 Квартира (Новостройка)", "🏘️ Квартира (Вторичная недвижимость)"],
        ["🏠 Дом", "🌿 Дача/Участок"],
        ["⬅️ Назад в меню"]
    ],
    resize_keyboard=True
)

apartment_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        ["Студия", "1к (Е-2)", "2к (Е-3)", "3к (Е-4)"],
        ["1-комнатная", "2-комнатная", "3-комнатная", "4-комнатная", "5-комнатная"],
        ["⬅️ Назад в меню"]
    ],
    resize_keyboard=True
)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "👋 Добро пожаловать в бот брокера Александра Суслова \"Недвижимость Тулы 24/7\"!\n\n"
        "Готов помочь с недвижимостью Тулы. Вы мечтаете — Я воплощаю! 💫",
        reply_markup=main_keyboard
    )

@app.on_message(filters.create(lambda _, m: m.text == "🏠 Хочу купить"))
async def buy(client, message):
    await message.reply_text("Что хотите купить?", reply_markup=buy_keyboard)

@app.on_message(filters.create(lambda _, m: m.text in ["🏢 Квартира (Новостройка)", "🏘️ Квартира (Вторичная недвижимость)"]))
async def choose_apartment(client, message):
    await message.reply_text("Выберите тип квартиры:", reply_markup=apartment_keyboard)

@app.on_message(filters.create(lambda _, m: m.text == "⬅️ Назад в меню"))
async def back(client, message):
    await message.reply_text("Вы вернулись в главное меню.", reply_markup=main_keyboard)

@app.on_message(filters.create(lambda _, m: m.text == "ℹ️ Обо мне"))
async def about(client, message):
    await message.reply_text(
        "👨‍💼 Александр Суслов\n"
        "📍 Специалист по недвижимости в Туле\n"
        "📱 [Связаться со мной](https://tapy.me/upfyk8)",
        disable_web_page_preview=True
    )

# ----------- Ночная проверка -----------

async def check_night_messages():
    moscow = pytz.timezone("Europe/Moscow")
    now = datetime.now(moscow)
    if 8 <= now.hour < 22:
        return  # Утро-день, не работаем

    await app.send_message(ADMIN_ID, "🛏️ Ночной режим: бот активен.")

# ----------- Основной запуск -----------

async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_night_messages, "interval", hours=1)
    scheduler.start()
    await app.start()
    await idle()
    await app.stop()

from pyrogram.idle import idle
asyncio.run(main())
