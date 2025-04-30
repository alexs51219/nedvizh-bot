from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from datetime import datetime
import pytz

user_data = {}

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
