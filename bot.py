import asyncio
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, time

# Настройки
API_ID = 12345678  # ← замени на свой API_ID
API_HASH = "your_api_hash_here"  # ← замени на свой API_HASH
BOT_TOKEN = "your_bot_token_here"  # ← замени на свой BOT_TOKEN
ADMIN_ID = 805696670  # ← твой Telegram ID

app = Client("nedvizh_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
scheduler = AsyncIOScheduler()

# --- Команды ---

# Старт
@app.on_message(filters.command("start"))
async def start(client, message: Message):
    keyboard = ReplyKeyboardMarkup(
        [["🏠 Хочу купить", "📤 Хочу продать"],
         ["ℹ️ Обо мне"]],
        resize_keyboard=True
    )
    await message.reply(
        "Добро пожаловать в бот «Недвижимость Тулы 24/7»!\n\nВыберите нужный пункт меню:",
        reply_markup=keyboard
    )

# Обо мне
@app.on_message(filters.text(["ℹ️ Обо мне"]))
async def about(client, message: Message):
    await message.reply(
        "Этот бот помогает быстро подобрать или продать недвижимость в Туле.\n"
        "🏡 Квартиры, дома, участки\n"
        "📞 Мы свяжемся с вами после заявки."
    )

# Хочу купить
@app.on_message(filters.text("🏠 Хочу купить"))
async def want_to_buy(client, message: Message):
    keyboard = ReplyKeyboardMarkup(
        [["🏢 Квартира (Новостройка)", "🏘️ Квартира (Вторичная недвижимость)"],
         ["🏡 Дом", "🌳 Участок/Дача"],
         ["🔙 Назад в меню"]],
        resize_keyboard=True
    )
    await message.reply("Что вы хотите купить?", reply_markup=keyboard)

# Назад в меню
@app.on_message(filters.text("🔙 Назад в меню"))
async def back_to_menu(client, message: Message):
    keyboard = ReplyKeyboardMarkup(
        [["🏠 Хочу купить", "📤 Хочу продать"],
         ["ℹ️ Обо мне"]],
        resize_keyboard=True
    )
    await message.reply("Возврат в главное меню:", reply_markup=keyboard)

# Новостройка
@app.on_message(filters.text("🏢 Квартира (Новостройка)"))
async def new_building(client, message: Message):
    keyboard = ReplyKeyboardMarkup(
        [["Студия", "1к (Е-2)", "2к (Е-3)", "3к (Е-4)", "Другое"],
         ["🔙 Назад в меню"]],
        resize_keyboard=True
    )
    await message.reply("Выберите тип квартиры (Новостройка):", reply_markup=keyboard)

# Вторичная недвижимость
@app.on_message(filters.text("🏘️ Квартира (Вторичная недвижимость)"))
async def secondary(client, message: Message):
    keyboard = ReplyKeyboardMarkup(
        [["1-комнатная", "2-комнатная", "3-комнатная", "4-комнатная", "5-комнатная"],
         ["Другое", "🔙 Назад в меню"]],
        resize_keyboard=True
    )
    await message.reply("Выберите тип квартиры (Вторичка):", reply_markup=keyboard)

# Фоновая задача — сообщение утром
async def morning_report():
    now = datetime.now()
    if now.time() >= time(8, 0):
        await app.send_message(ADMIN_ID, "☀️ Бот проснулся. Готов к приёму заявок!")

# Запуск
async def main():
    scheduler.add_job(morning_report, "cron", hour=8, minute=0)
    scheduler.start()
    await app.start()
    print("Бот запущен.")
    await asyncio.get_event_loop().create_future()  # бесконечное ожидание

if __name__ == "__main__":
    asyncio.run(main())
