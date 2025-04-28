import asyncio
import pytz
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton

app = Client(
    "nedvizh_bot",
    api_id=28155507,
    api_hash="cce39d7743018b7c5b2047757ce85eee",
    bot_token="7949703718:AAH43G5ZyQ_vDxRD3LG6sUFz09rOPkfvXGA"
)

ADMIN_ID = 805696670  # ← Твой ID

def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("🏠 Хочу купить")],
            [KeyboardButton("🏡 Хочу продать")],
            [KeyboardButton("ℹ️ Обо мне")]
        ],
        resize_keyboard=True
    )

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "👋 Добро пожаловать в бот брокера Александра Суслова \"Недвижимость Тулы 24/7\"!\n\n"
        "Готов помочь с недвижимостью Тулы.\nВы мечтаете — Я воплощаю! 💫",
        reply_markup=main_menu()
    )

# --- Обработка кнопки "🏠 Хочу купить" ---
@app.on_message(filters.regex("🏠 Хочу купить"))
async def buy_property(client, message):
    await message.reply_text(
        "Что вас интересует?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton("🏢 Квартира (Новостройка)"), KeyboardButton("🏘️ Квартира (Вторичная недвижимость)")],
                [KeyboardButton("🏡 Дом"), KeyboardButton("🌳 Дача / Участок")],
                [KeyboardButton("🔙 Назад в меню")]
            ],
            resize_keyboard=True
        )
    )

# --- Обработка кнопки "🏡 Хочу продать" ---
@app.on_message(filters.regex("🏡 Хочу продать"))
async def sell_property(client, message):
    await message.reply_text(
        "Отлично! Пожалуйста, отправьте основные данные о недвижимости, которую хотите продать.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton("🔙 Назад в меню")]
            ],
            resize_keyboard=True
        )
    )

# --- Обработка кнопки "ℹ️ Обо мне" ---
@app.on_message(filters.regex("ℹ️ Обо мне"))
async def about_me(client, message):
    await message.reply_text(
        "📞 Мои контакты:\n"
        "https://tapy.me/upfyk8",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton("🔙 Назад в меню")]
            ],
            resize_keyboard=True
        )
    )

# --- Новое! Обработка кнопки "🔙 Назад в меню" ---
@app.on_message(filters.regex("🔙 Назад в меню"))
async def back_to_menu(client, message):
    await message.reply_text(
        "Вы в главном меню. Выберите действие:",
        reply_markup=main_menu()
    )

# --- Работа ночью и запись ночных сообщений ---
async def send_reminders():
    tz = pytz.timezone('Europe/Moscow')
    while True:
        now = datetime.now(tz)
        if now.hour == 8 and now.minute == 0:
            try:
                with open("night_contacts.txt", "r", encoding="utf-8") as file:
                    contacts = file.read().strip()
                if contacts:
                    await app.send_message(ADMIN_ID, f"🌙 Ночные обращения:\n\n{contacts}")
                    open("night_contacts.txt", "w", encoding="utf-8").close()
            except FileNotFoundError:
                pass
        await asyncio.sleep(60)

@app.on_message()
async def handle_all_messages(client, message):
    tz = pytz.timezone('Europe/Moscow')
    now = datetime.now(tz)
    if 22 <= now.hour or now.hour < 8:
        await message.reply_text("🌙 Бот сейчас отдыхает. Ваш запрос сохранён, я отвечу утром! ☀️")
        with open("night_contacts.txt", "a", encoding="utf-8") as file:
            file.write(f"{message.from_user.first_name} (@{message.from_user.username}) - {message.text}\n")
    else:
        pass

async def main():
    await app.start()
    await send_reminders()

if __name__ == "__main__":
    app.run()
