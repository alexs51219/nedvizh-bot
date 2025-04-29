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
ADMIN_ID = 805696670  # ← Твой Telegram ID

app = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# --- Главное меню ---
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        ["🏠 Хочу купить", "🏘️ Хочу продать"],
        ["ℹ️ Обо мне"]
    ],
    resize_keyboard=True
)

# --- Кнопки "Хочу купить" ---
buy_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        ["🏢 Квартира (Новостройка)", "🏘️ Квартира (Вторичная недвижимость)"],
        ["🏠 Дом", "🌿 Дача/Участок"],
        ["⬅️ Назад в меню"]
    ],
    resize_keyboard=True
)

# --- Кнопки выбора квартир ---
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
        "Готов помочь с недвижимостью Тулы.\n"
        "Вы мечтаете — Я воплощаю! 💫",
        reply_markup=main_keyboard
    )

@app.on_message(filters.create(lambda _, m: m.text == "🏠 Хочу купить"))
async def buy(client, message):
    await message.reply_text("Что хотите купить?", reply_markup=buy_keyboard)

@app.on_message(filters.create(lambda _, m: m.text in ["🏢 Квартира (Новостройка)", "🏘️ Квартира (Вторичная недвижимость)"]))
async def choose_apartment(client, message):
    await message.reply_text("Выберите тип квартиры:", reply_markup=apartment_keyboard)

@app.on_message(filters.create(lambda _, m: m.text == "⬅️ Назад в меню"))
async def back_to_menu(client, message):
    await message.reply_text("Главное меню:", reply_markup=main_keyboard)

@app.on_message(filters.create(lambda _, m: m.text == "ℹ️ Обо мне"))
async def about_me(client, message):
    await message.reply_text(
        "👨‍💼 Александр Суслов\n"
        "📍 Специалист по недвижимости в Туле\n"
        "📱 [Связаться со мной](https://tapy.me/upfyk8)",
        disable_web_page_preview=True
    )

# --- Функция ночной активности (упрощённая версия) ---
async def night_task():
    while True:
        moscow = pytz.timezone("Europe/Moscow")
        now = datetime.now(moscow)
        if 22 <= now.hour or now.hour < 8:
            # Ночь
            await app.send_message(ADMIN_ID, "🌙 Ночной режим активирован.")
        await asyncio.sleep(3600)  # проверять каждый час

if __name__ == "__main__":
    scheduler = AsyncIOScheduler()
    scheduler.start()
    app.run()
