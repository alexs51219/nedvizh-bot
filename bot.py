import asyncio
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import pytz

# Заменить на свой Telegram ID
ADMIN_ID = 805696670

# Настройка клиента
app = Client(
    "nedvizh_bot",
    api_id=123456,  # 👉 твои значения
    api_hash="abc123",  # 👉 твои значения
    bot_token="your_bot_token_here"  # 👉 токен бота
)

# Главное меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("🏠 Хочу купить"), KeyboardButton("💼 Хочу продать")],
        [KeyboardButton("ℹ️ Обо мне")]
    ],
    resize_keyboard=True
)

# Стартовое сообщение
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "👋 Добро пожаловать в бот брокера (специалиста по недвижимости) Александра Суслова \"Недвижимость Тулы 24/7\"!\n\n"
        "Готов помочь с недвижимостью Тулы.\nВы мечтаете — Я воплощаю! 💫",
        reply_markup=main_menu
    )

# Обработка "Обо мне"
@app.on_message(filters.text(["ℹ️ Обо мне"]))
async def about(client, message):
    await message.reply_text("🔗 Мои контакты: https://tapy.me/upfyk8")

# Обработка "Хочу купить"
@app.on_message(filters.text(["🏠 Хочу купить"]))
async def buy(client, message):
    await message.reply_text(
        "Что вы хотите купить?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton("🏢 Квартира (Новостройка)"), KeyboardButton("🏘️ Квартира (Вторичная недвижимость)")],
                [KeyboardButton("🏡 Дом / Дача"), KeyboardButton("🌿 Земельный участок")],
                [KeyboardButton("⬅️ Назад в меню")]
            ],
            resize_keyboard=True
        )
    )

# Назад в меню
@app.on_message(filters.text(["⬅️ Назад в меню"]))
async def back_to_menu(client, message):
    await message.reply_text("Главное меню", reply_markup=main_menu)

# Планировщик задач
scheduler = AsyncIOScheduler(timezone=pytz.timezone('Europe/Moscow'))

# Утренняя проверка
async def morning_check():
    now = datetime.now(pytz.timezone("Europe/Moscow"))
    if now.hour == 8:
        await app.send_message(ADMIN_ID, "☀️ Бот вышел из режима сна и готов к работе!")

# Задание каждый час
scheduler.add_job(morning_check, "interval", minutes=60)

# Запуск бота
async def main():
    await app.start()
    scheduler.start()
    print("Бот запущен")
    await idle()

from pyrogram import idle
asyncio.run(main())
