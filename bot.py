from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from datetime import datetime
import pytz

# 🔐 Данные авторизации
api_id = 28155507
api_hash = "cce39d7743018b7c5b2047757ce85eee"
bot_token = "7949703718:AAH43G5ZyQ_vDxRD3LG6sUFz09rOPkfvXGA"

app = Client("nedvizh_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# 🌙 Временной режим работы
SLEEP_START = 22  # 22:00
SLEEP_END = 8     # 08:00
user_data = {}
night_users = set()
greeting_sent = set()

def is_sleep_time():
    tz = pytz.timezone('Europe/Moscow')
    current_hour = datetime.now(tz).hour
    return current_hour >= SLEEP_START or current_hour < SLEEP_END

@app.on_message(filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id

    # 💬 Приветствие (один раз утром тем, кто писал ночью)
    if user_id in night_users and user_id not in greeting_sent and not is_sleep_time():
        await message.reply("☀️ Доброе утро! Вы писали ночью, теперь я снова в деле.")
        greeting_sent.add(user_id)

    # 💤 Ответ в ночное время
    if is_sleep_time():
        night_users.add(user_id)
        await message.reply("😴 Бот сейчас отдыхает с 22:00 до 08:00. Ответим с утра!")
        return

    # Главное меню
    keyboard = ReplyKeyboardMarkup(
        [["🏠 Хочу купить", "📤 Хочу продать"],
         ["ℹ️ Обо мне"]],
        resize_keyboard=True
    )
    await message.reply(
        "👋 Добро пожаловать в бот брокера (специалиста по недвижимости) Александра Суслова «Недвижимость Тулы 24/7»!\n\n"
        "Готов помочь с недвижимостью Тулы. Вы мечтаете — Я воплощаю! 💫",
        reply_markup=keyboard
    )

@app.on_message(filters.text("ℹ️ Обо мне"))
async def about_me(client, message):
    await message.reply("🔗 Мои контакты: https://tapy.me/upfyk8")

# 🏠 Анкета: Хочу купить
@app.on_message(filters.text("🏠 Хочу купить"))
async def start_purchase(client, message):
    user_id = message.from_user.id
    user_data[user_id] = {}
    
    # Вопрос 1: тип недвижимости
    reply_markup = ReplyKeyboardMarkup(
        [
            ["Квартира", "Дом"],
            ["Дача", "Земельный участок"],
            ["Другое"]
        ], resize_keyboard=True, one_time_keyboard=True
    )
    await message.reply("🏘️ Какой тип недвижимости вас интересует?", reply_markup=reply_markup)
    app.register_next_step_handler(message, handle_property_type)

async def handle_property_type(message):
    user_id = message.from_user.id
    user_data[user_id]["Тип недвижимости"] = message.text

    if message.text == "Квартира":
        reply_markup = ReplyKeyboardMarkup(
            [["Новостройка", "Вторичная недвижимость"]],
            resize_keyboard=True, one_time_keyboard=True
        )
        await message.reply("🏗️ Уточните тип квартиры:", reply_markup=reply_markup)
        app.register_next_step_handler(message, handle_flat_category)
    else:
        await message.reply("🏗️ Следующие шаги для выбранного типа скоро появятся.")

# (Следующие шаги анкеты — добавим в следующей части)

# ▶️ Запуск бота
app.run()
