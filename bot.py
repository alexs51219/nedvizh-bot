import os
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup

# Берём данные из переменных окружения
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")

app = Client("nedvizh247_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        ["🏠 Хочу купить", "📤 Хочу продать"]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply(
        "👋 Добро пожаловать в бот 'Недвижимость 24/7'!\n\n"
        "Выберите, что вы хотите сделать:",
        reply_markup=main_menu
    )

@app.on_message(filters.regex("Хочу купить"))
async def handle_buy(client, message):
    await message.reply("🛒 Отлично! Сейчас подберём вам недвижимость...\n(в будущем добавим фильтры)")

@app.on_message(filters.regex("Хочу продать"))
async def handle_sell(client, message):
    await message.reply("📋 Отлично! Сейчас оформим вашу заявку на продажу...\n(в будущем — сбор параметров)")

app.run()
