import os
import datetime
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup
import pytz
import time
import requests

# ==== Фейковый сервер для Render ====
def run_fake_server():
    server = HTTPServer(("0.0.0.0", 10000), SimpleHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=run_fake_server, daemon=True).start()

# ==== Автопинг для Render ====
def keep_alive():
    def ping():
        while True:
            try:
                requests.get("http://127.0.0.1:10000")
            except Exception as e:
                print(f"Ping error: {e}")
            time.sleep(1500)  # 25 минут

    threading.Thread(target=ping, daemon=True).start()

keep_alive()

# ==== Настройки ====
SLEEP_START = 22
SLEEP_END = 8
moscow = pytz.timezone("Europe/Moscow")
night_users = []

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

admin_user_id = 794970371  # 🔥 Здесь укажи свой Telegram ID (без восьмёрки в начале)

# ==== Вспомогательные функции ====
def is_night_time():
    now = datetime.datetime.now(moscow).time()
    return now.hour >= SLEEP_START or now.hour < SLEEP_END

async def send_morning_summary():
    now = datetime.datetime.now(moscow)
    if now.hour == SLEEP_END and night_users:
        text = "🌙 Ночные заявки:\n\n"
        for user in night_users:
            text += f"• {user['name']} (@{user['username']}) в {user['time']}\n"
        try:
            await app.send_message(admin_user_id, text)
        except Exception as e:
            print(f"Ошибка отправки ночного отчёта: {e}")
        night_users.clear()

def log_night_user(user):
    if not user:
        return
    user_id = user.id
    username = user.username or "нет username"
    name = user.first_name or "без имени"
    now_time = datetime.datetime.now(moscow).strftime("%H:%M")
    # Проверка, чтобы не добавлять дубли
    if not any(u['user_id'] == user_id for u in night_users):
        night_users.append({
            "user_id": user_id,
            "username": username,
            "name": name,
            "time": now_time
        })

# ==== Обработчики сообщений ====
@app.on_message(filters.command("start"))
async def start(client, message):
    await send_morning_summary()
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
    await send_morning_summary()
    if is_night_time():
        log_night_user(message.from_user)
        await message.reply("🌙 Бот сейчас спит. Пожалуйста, напишите с 08:00 до 22:00. Спасибо!")
    else:
        await message.reply("🛒 Отлично! Сейчас подберём вам недвижимость...\n(в дальнейшем будет фильтрация по параметрам)")

@app.on_message(filters.regex("Хочу продать"))
async def handle_sell(client, message):
    await send_morning_summary()
    if is_night_time():
        log_night_user(message.from_user)
        await message.reply("🌙 Бот сейчас спит. Пожалуйста, напишите с 08:00 до 22:00. Спасибо!")
    else:
        await message.reply("📋 Отлично! Сейчас оформим вашу заявку на продажу...\n(в дальнейшем — сбор параметров)")

@app.on_message(filters.regex("Обо мне"))
async def about_me(client, message):
    await message.reply("ℹ️ Подробнее обо мне: https://tapy.me/upfyk8")

app.run()
