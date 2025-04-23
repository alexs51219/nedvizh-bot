import os
import datetime
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup
import asyncio
import pytz  # Добавили pytz

# ==== Фейковый сервер для Render ====
def run_fake_server():
    server = HTTPServer(("0.0.0.0", 10000), SimpleHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=run_fake_server, daemon=True).start()

# ==== Настройки ====
SLEEP_START = 22
SLEEP_END = 8
NIGHT_LOG_FILE = "night_contacts.txt"
moscow = pytz.timezone("Europe/Moscow")

# ==== Авторизация ====
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")

app = Client("nedvizh247_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        ["🏠 Хочу купить", "📤 Хочу продать"],
        ["ℹ️ Обо мне"]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

def is_night_time():
    now = datetime.datetime.now(moscow).time()
    return now.hour >= SLEEP_START or now.hour < SLEEP_END

def log_night_user(user):
    if not user:
        return
    user_id = user.id
    username = user.username or "нет username"
    name = user.first_name or "без имени"
    now = datetime.datetime.now(moscow).strftime("%Y-%m-%d %H:%M")
    line = f"{user_id} | @{username} | {name} | {now} | reminder_sent: False\n"
    if os.path.exists(NIGHT_LOG_FILE):
        with open(NIGHT_LOG_FILE, "r", encoding="utf-8") as file:
            if str(user_id) in file.read():
                return
    with open(NIGHT_LOG_FILE, "a", encoding="utf-8") as file:
        file.write(line)

async def send_reminders():
    if not os.path.exists(NIGHT_LOG_FILE):
        return
    updated_lines = []
    async with app:
        with open(NIGHT_LOG_FILE, "r", encoding="utf-8") as file:
            for line in file.readlines():
                if "reminder_sent: False" in line:
                    try:
                        user_id = int(line.split("|")[0].strip())
                        await app.send_message(user_id, "🌞 Доброе утро! Вы писали нам ночью. Готовы продолжить?")
                        line = line.replace("reminder_sent: False", "reminder_sent: True")
                    except Exception as e:
                        print(f"Не удалось отправить напоминание пользователю {user_id}: {e}")
                updated_lines.append(line)
        with open(NIGHT_LOG_FILE, "w", encoding="utf-8") as file:
            file.writelines(updated_lines)

@app.on_message(filters.command("start"))
async def start(client, message):
    await send_reminders()
    if is_night_time():
        log_night_user(message.from_user)
        await message.reply("🌙 Бот сейчас спит. Пожалуйста, напишите с 08:00 до 22:00. Спасибо!")
    else:
        await message.reply(
            "👋 Добро пожаловать в бот брокера (специалиста по недвижимости) Александра Суслова \"Недвижимость Тулы 24/7\"!\n\n"
            "Готов помочь с недвижимостью Тулы.\n"
            "Вы мечтаете — Я воплощаю! 💫",
            reply_markup=main_menu
        )

@app.on_message(filters.regex("Хочу купить"))
async def handle_buy(client, message):
    if is_night_time():
        log_night_user(message.from_user)
        await message.reply("🌙 Бот сейчас спит. Пожалуйста, напишите с 08:00 до 22:00. Спасибо!")
    else:
        await message.reply("🛒 Отлично! Сейчас подберём вам недвижимость...\n(в дальнейшем будет фильтрация по параметрам)")

@app.on_message(filters.regex("Хочу продать"))
async def handle_sell(client, message):
    if is_night_time():
        log_night_user(message.from_user)
        await message.reply("🌙 Бот сейчас спит. Пожалуйста, напишите с 08:00 до 22:00. Спасибо!")
    else:
        await message.reply("📋 Отлично! Сейчас оформим вашу заявку на продажу...\n(в дальнейшем — сбор параметров)")

@app.on_message(filters.regex("Обо мне"))
async def about_me(client, message):
    await message.reply("ℹ️ Подробнее обо мне: https://tapy.me/upfyk8")

app.run()
