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

        if text == "Квартира (Новостройка)":
            user_forms[user_id]["stage"] = "apartment_type_new"

            await message.reply(
                "Какой тип квартиры вас интересует? 🏢 (Новостройка)\n\n"
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

        elif text == "Квартира (Вторичная недвижимость)":
            user_forms[user_id]["stage"] = "apartment_type_secondary"

            await message.reply(
                "Какой тип квартиры вас интересует? 🏢 (Вторичная недвижимость)\n\n"
                "Выберите один из вариантов или напишите свой вариант ✏️",
                reply_markup=ReplyKeyboardMarkup(
                    [
                        ["1-комнатная", "2-комнатная"],
                        ["3-комнатная", "4-комнатная"],
                        ["Другое"]
                    ],
                    resize_keyboard=True
                )
            )

        else:
            # Если выбрали Дом, Дачу или Участок — пока просто фиксация
            user_forms[user_id]["stage"] = "done"
            await message.reply("Отлично! 📝 (Следующие вопросы скоро будут подключены.)")

    elif stage in ["apartment_type_new", "apartment_type_secondary"]:
        user_forms[user_id]["apartment_type"] = text

        await message.reply("Отлично! 📝 (Следующие вопросы скоро будут подключены.)")
