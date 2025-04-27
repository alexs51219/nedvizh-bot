# Словарь для хранения анкет пользователей
user_forms = {}

# Старт анкеты
@app.on_message(filters.regex("🏠 Хочу купить"))
async def start_buy_form(client, message):
    user_id = message.from_user.id
    user_forms[user_id] = {"stage": "property_type"}

    await message.reply(
        "Что хотите купить? 🏠\n\n"
        "Выберите один из вариантов или напишите свой вариант ✏️",
        reply_markup=ReplyKeyboardMarkup(
            [
                ["Квартира (Вторичная недвижимость)", "Квартира (Новостройка)"],
                ["Дом", "Дача"],
                ["Земельный участок", "Другое"]
            ],
            resize_keyboard=True
        )
    )

# Обработка всех текстовых сообщений
@app.on_message(filters.text & ~filters.command("start"))
async def handle_form(client, message):
    user_id = message.from_user.id

    if user_id not in user_forms:
        return

    stage = user_forms[user_id]["stage"]
    text = message.text

    if stage == "property_type":
        user_forms[user_id]["property_type"] = text
        user_forms[user_id]["stage"] = "apartment_type"

        await message.reply(
            "Какой тип недвижимости вас интересует? 🏢\n\n"
            "Выберите один из вариантов или напишите свой вариант ✏️",
            reply_markup=ReplyKeyboardMarkup(
                [
                    ["Студия", "1к (Е-2)"],
                    ["2к (Е-3)", "3к (Е-4)"],
                    ["4к и более", "Другое"]
                ],
                resize_keyboard=True
            )
        )

    elif stage == "apartment_type":
        user_forms[user_id]["apartment_type"] = text

        await message.reply("Отлично! 📝 (Следующие вопросы скоро будут подключены.)")
