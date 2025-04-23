from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup

api_id = 28155507
api_hash = "cce39d7743018b7c5b2047757ce85eee"
bot_token = "7949703718:AAH43G5ZyQ_vDxRD3LG6sUFz09rOPkfvXGA"

app = Client("nedvizh247_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Главное меню
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
    await message.reply("🛒 Отлично! Сейчас подберём вам недвижимость...\n(в дальнейшем будет фильтрация по параметрам)")

@app.on_message(filters.regex("Хочу продать"))
async def handle_sell(client, message):
    await message.reply("📋 Отлично! Сейчас оформим вашу заявку на продажу...\n(в дальнейшем — сбор параметров)")

app.run()
