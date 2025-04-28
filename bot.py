from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import pytz
import asyncio
import os

# Данные для подключения
API_ID = 28155507
API_HASH = "cce39d7743018b7c5b2047757ce85eee"
BOT_TOKEN = "7949703718:AAH43G5ZyQ_vDxRD3LG6sUFz09rOPkfvXGA"
ADMIN_ID = 805696670

app = Client("nedvizh_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Главное меню
menu = ReplyKeyboardMarkup(
    keyboard=[
        ["🏠 Хочу купить", "🏡 Хочу продать"],
        ["ℹ️ Обо мне"]
    ],
    resize_keyboard=True
)

# Стартовое сообщение
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply(
        "👋 Добро пожаловать в бот брокера (специалиста по недвижимости) Александра Суслова \"Недвижимость Тулы 24/7\"!\n\n"
        "Готов помочь с недвижимостью Тулы.\n"
        "Вы мечтаете — Я воплощаю! 💫\n\n"
        "Выберите, пожалуйста, действие ниже ⬇️",
        reply_markup=menu
    )

# Ответ на кнопку "Обо мне"
@app.on_message(filters.text("ℹ️ Обо мне"))
async def about(client, message):
    await message.reply("🔗 Подробнее обо мне: https://tapy.me/upfyk8")

# Спящий режим
tz = pytz.timezone('Europe/Moscow')

async def is_sleep_time():
    now = datetime.now(tz)
    return now.hour >= 22 or now.hour < 8

# Ответы на кнопки "Хочу купить" и "Хочу продать"
@app.on_message(filters.text(["🏠 Хочу купить", "🏡 Хочу продать"]))
async def handle_menu(client, message):
    if await is_sleep_time():
        await message.reply("😴 Бот спит с 22:00 до 08:00. Ваша заявка будет обработана утром!")
        save_night_request(message)
    else:
        if message.text == "🏠 Хочу купить":
            await message.reply(
                "Что именно хотите купить?",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[
                        ["🏢 Квартира (Новостройка)", "🏘️ Квартира (Вторичная недвижимость)"],
                        ["🏠 Дом", "🏡 Дача", "🌿 Земельный участок"],
                        ["🏡 Другое", "⬅️ Назад в меню"]
                    ],
                    resize_keyboard=True
                )
            )
        elif message.text == "🏡 Хочу продать":
            await message.reply(
                "Что именно хотите продать?",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[
                        ["🏢 Квартира (Новостройка)", "🏘️ Квартира (Вторичная недвижимость)"],
                        ["🏠 Дом", "🏡 Дача", "🌿 Земельный участок"],
                        ["🏡 Другое", "⬅️ Назад в меню"]
                    ],
                    resize_keyboard=True
                )
            )

# Обработка кнопки "Назад в меню"
@app.on_message(filters.text("⬅️ Назад в меню"))
async def back_to_main_menu(client, message):
    await message.reply("Вы вернулись в главное меню.", reply_markup=menu)

# Сохраняем ночные заявки
def save_night_request(message):
    with open("night_requests.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now(tz).strftime('%d.%m.%Y %H:%M:%S')} - {message.from_user.id} - {message.text}\n")

# Утренняя отправка списка ночных заявок
async def send_morning_report():
    if os.path.exists("night_requests.txt"):
        with open("night_requests.txt", "r", encoding="utf-8") as f:
            requests = f.read()
        if requests:
            await app.send_message(ADMIN_ID, f"🌅 Ночные заявки:\n\n{requests}")
            open("night_requests.txt", "w", encoding="utf-8").close()

# Планировщик для утреннего отчёта
scheduler = AsyncIOScheduler()

scheduler.add_job(send_morning_report, "cron", hour=8, minute=0, timezone=tz)

scheduler.start()

# Запуск
app.run()
