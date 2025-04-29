import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz
from datetime import datetime
import os

API_ID = 12345678  # <-- твой настоящий API_ID
API_HASH = "your_api_hash"  # <-- твой настоящий API_HASH
BOT_TOKEN = "your_bot_token"  # <-- твой настоящий BOT_TOKEN
ADMIN_ID = 805696670  # <-- твой Telegram ID (ты присылал!)

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

logging.basicConfig(level=logging.INFO)

# Путь для сохранения ночных заявок
NIGHT_REQUESTS_FILE = "night_requests.txt"

# Таймзона
tz = pytz.timezone('Europe/Moscow')

# Время работы
WORK_START = 8
WORK_END = 22

# Команда /start
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply(
        "👋 Добро пожаловать в бот брокера (специалиста по недвижимости) Александра Суслова \"Недвижимость Тулы 24/7\"!\n\n"
        "Готов помочь с недвижимостью Тулы. Вы мечтаете — Я воплощаю! 💫",
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton("🏠 Хочу купить"), KeyboardButton("🏡 Хочу продать")],
                [KeyboardButton("ℹ️ Обо мне")]
            ],
            resize_keyboard=True
        )
    )

# Кнопка "Обо мне"
@app.on_message(filters.text(["ℹ️ Обо мне"]))
async def about(client, message):
    await message.reply("🔗 Подробнее: https://tapy.me/upfyk8")

# Кнопка "Хочу купить"
@app.on_message(filters.text("🏠 Хочу купить"))
async def buy(client, message):
    await message.reply(
        "Выберите, что хотите купить:",
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton("🏢 Квартира (Новостройка)"), KeyboardButton("🏘️ Квартира (Вторичная недвижимость)")],
                [KeyboardButton("🏠 Дом / Дача"), KeyboardButton("🌳 Земельный участок")],
                [KeyboardButton("↩️ Назад в меню")]
            ],
            resize_keyboard=True
        )
    )

# Кнопка "Хочу продать"
@app.on_message(filters.text("🏡 Хочу продать"))
async def sell(client, message):
    await message.reply("💬 Напишите, что хотите продать, и я с вами свяжусь!")

# Кнопка "Назад в меню"
@app.on_message(filters.text("↩️ Назад в меню"))
async def back_to_menu(client, message):
    await start(client, message)

# Обработка выбора квартир
@app.on_message(filters.text(["🏢 Квартира (Новостройка)", "🏘️ Квартира (Вторичная недвижимость)"]))
async def select_apartment_type(client, message):
    if message.text == "🏢 Квартира (Новостройка)":
        await message.reply(
            "Выберите тип квартиры в новостройке:",
            reply_markup=ReplyKeyboardMarkup(
                [
                    [KeyboardButton("Студия"), KeyboardButton("1к (Е-2)")],
                    [KeyboardButton("2к (Е-3)"), KeyboardButton("3к (Е-4)")],
                    [KeyboardButton("Другое"), KeyboardButton("↩️ Назад в меню")]
                ],
                resize_keyboard=True
            )
        )
    else:
        await message.reply(
            "Выберите тип квартиры на вторичном рынке:",
            reply_markup=ReplyKeyboardMarkup(
                [
                    [KeyboardButton("1-комнатная"), KeyboardButton("2-комнатная")],
                    [KeyboardButton("3-комнатная"), KeyboardButton("4-комнатная")],
                    [KeyboardButton("5-комнатная"), KeyboardButton("Другое")],
                    [KeyboardButton("↩️ Назад в меню")]
                ],
                resize_keyboard=True
            )
        )

# Отправка сообщения ночью
@app.on_message(filters.private & ~filters.command(["start"]))
async def handle_message(client, message):
    now = datetime.now(tz)
    if WORK_START <= now.hour < WORK_END:
        pass  # Бот работает нормально
    else:
        # Сохраняем ночную заявку
        with open(NIGHT_REQUESTS_FILE, "a", encoding="utf-8") as file:
            file.write(f"{datetime.now(tz)} — {message.from_user.first_name} (@{message.from_user.username}) — {message.text}\n")
        await message.reply("Бот сейчас отдыхает. 💤 Я обязательно свяжусь с вами утром!")

# Ежедневная проверка ночных заявок
async def send_night_requests():
    if os.path.exists(NIGHT_REQUESTS_FILE):
        with open(NIGHT_REQUESTS_FILE, "r", encoding="utf-8") as file:
            requests = file.read()
        if requests:
            await app.send_message(ADMIN_ID, f"🌙 Ночные обращения:\n\n{requests}")
        os.remove(NIGHT_REQUESTS_FILE)

scheduler = AsyncIOScheduler()
scheduler.add_job(send_night_requests, "cron", hour=WORK_START, minute=0, timezone=tz)
scheduler.start()

print("Бот запущен...")
app.run()
