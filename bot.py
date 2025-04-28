from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup

app = Client(
    "nedvizh_bot",
    bot_token="7949703718:AAH43G5ZyQ_vDxRD3LG6sUFz09rOPkfvXGA",
    api_id=28155507,
    api_hash="cce39d7743018b7c5b2047757ce85eee"
)

# --- Приветствие ---
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply(
        "👋 Добро пожаловать в бот брокера (специалиста по недвижимости) Александра Суслова 'Недвижимость Тулы 24/7'!\n\nГотов помочь с недвижимостью Тулы.\nВы мечтаете — Я воплощаю! 💫",
        reply_markup=ReplyKeyboardMarkup(
            [
                ["🏠 Хочу купить", "🏡 Хочу продать"],
                ["ℹ️ Обо мне"]
            ],
            resize_keyboard=True
        )
    )

# --- Выбор что купить ---
@app.on_message(filters.regex("🏠 Хочу купить"))
async def want_to_buy(client, message):
    await message.reply(
        "Что вы хотите купить?",
        reply_markup=ReplyKeyboardMarkup(
            [
                ["🏢 Квартира (Новостройка)", "🏘️ Квартира (Вторичная недвижимость)"],
                ["🏡 Дом", "🏡 Дача", "🌱 Земельный участок"],
                ["🔎 Другое"],
                ["🔙 Назад в меню"]
            ],
            resize_keyboard=True
        )
    )

# --- Выбор типа квартиры ---
@app.on_message(filters.regex("🏢 Квартира \\(Новостройка\\)|🏘️ Квартира \\(Вторичная недвижимость\\)"))
async def choose_flat_type(client, message):
    if message.text == "🏢 Квартира (Новостройка)":
        await message.reply(
            "Выберите тип квартиры в новостройке:",
            reply_markup=ReplyKeyboardMarkup(
                [
                    ["Студия", "1к (Е-2)"],
                    ["2к (Е-3)", "3к (Е-4)"],
                    ["Другое"],
                    ["🔙 Назад в меню"]
                ],
                resize_keyboard=True
            )
        )
    else:
        await message.reply(
            "Выберите тип квартиры на вторичном рынке:",
            reply_markup=ReplyKeyboardMarkup(
                [
                    ["1-комнатная", "2-комнатная"],
                    ["3-комнатная", "4-комнатная"],
                    ["5-комнатная", "Другое"],
                    ["🔙 Назад в меню"]
                ],
                resize_keyboard=True
            )
        )

# --- Площадь квартиры ---
@app.on_message(filters.text(["Студия", "1к (Е-2)", "2к (Е-3)", "3к (Е-4)", "1-комнатная", "2-комнатная", "3-комнатная", "4-комнатная", "5-комнатная"]))
async def ask_flat_area(client, message):
    await message.reply(
        "Выберите желаемую площадь квартиры:",
        reply_markup=ReplyKeyboardMarkup(
            [
                ["до 30 м²", "30–50 м²"],
                ["50–70 м²", "70–100 м²"],
                ["100+ м²"],
                ["🔙 Назад в меню"]
            ],
            resize_keyboard=True
        )
    )

# --- Запуск приложения ---
app.run()
