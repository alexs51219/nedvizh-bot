import asyncio
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import pytz
import os

# Твои данные
API_ID = 28155507
API_HASH = "cce39d7743018b7c5b2047757ce85eee"
BOT_TOKEN = "7949703718:AAH43G5ZyQ_vDxRD3LG6sUFz09rOPkfvXGA"
ADMIN_ID = 805696670  # <-- Вставил твой Telegram ID!

# Время для работы бота
TIMEZONE = pytz.timezone('Europe/Moscow')

# Инициализация бота
app = Client(
    "nedvizh_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Главное меню
menu = ReplyKeyboardMarkup(
    [
        ["🏠 Хочу купить"],
        ["📤 Хочу продать"],
        ["ℹ️ Обо мне"]
    ],
    resize_keyboard=True
)

# Добро пожаловать
WELCOME_TEXT = (
    "👋 Добро пожаловать в бот брокера (специалиста по недвижимости) Александра Суслова "
    "«Недвижимость Тулы 24/7»!\n\n"
    "Готов помочь с недвижимостью Тулы.\n"
    "Вы мечтаете — Я воплощаю! 💫"
)

# Функция для отправки ночных контактов утром
async def send_night_contacts():
    contacts_file = "night_contacts.txt"

    if os.path.exists(contacts_file):
        with open(contacts_file, "r", encoding="utf-8") as file:
            contacts = file.read()

        if contacts.strip():
            await app.send_message(
                ADMIN_ID,
                f"🌙 Ночные заявки:\n\n{contacts}"
            )
        else:
            await app.send_message(
                ADMIN_ID,
                "🌙 Ночных заявок не было."
            )

        with open(contacts_file, "w", encoding="utf-8") as file:
            file.write("")
    else:
        await app.send_message(
            ADMIN_ID,
            "🌙 Файл ночных заявок не найден."
        )

# Утренняя задача
async def morning_tasks():
    await send_night_contacts()

# Планировщик работы
scheduler = AsyncIOScheduler()

def start_scheduler():
    now = datetime.now(TIMEZONE)
    current_hour = now.hour

    # Время пробуждения 08:00
    if 8 <= current_hour < 22:
        scheduler.add_job(send_reminders, "interval", minutes=120)
    else:
        scheduler.add_job(sleep_mode, "interval", minutes=5)

    scheduler.start()

async def send_reminders():
    pass  # Здесь твои напоминания если надо

async def sleep_mode():
    pass  # Спящий режим

# Обработка команд
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply(WELCOME_TEXT, reply_markup=menu)
    await morning_tasks()

@app.on_message(filters.regex("🏠 Хочу купить"))
async def buy(client, message):
    await message.reply("🏠 Отлично! Сейчас поможем подобрать недвижимость.\n(Анкета скоро будет подключена!)")

@app.on_message(filters.regex("📤 Хочу продать"))
async def sell(client, message):
    await message.reply("📤 Отлично! Расскажите о своём объекте.\n(Анкета скоро будет подключена!)")

@app.on_message(filters.regex("ℹ️ Обо мне"))
async def about(client, message):
    await message.reply(
        "🔗 Вот мои контакты:\nhttps://tapy.me/upfyk8",
        disable_web_page_preview=False
    )

# Запуск
if __name__ == "__main__":
    app.run()
