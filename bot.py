import random
import asyncio
import json
import os

from datetime import time
from zoneinfo import ZoneInfo

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

from telegram.error import BadRequest

TOKEN = os.getenv("BOT_TOKEN")


# ---------- ФУНКЦИЯ СОХРАНЕНИЯ ПОЛЬЗОВАТЕЛЯ ----------
def save_user(chat_id):
    if not os.path.exists("users.json"):
        with open("users.json", "w") as f:
            json.dump([], f)

    with open("users.json", "r") as f:
        users = json.load(f)

    if chat_id not in users:
        users.append(chat_id)

        with open("users.json", "w") as f:
            json.dump(users, f)


# ---------- ХАКЕРСКИЙ ЭФФЕКТ ----------
async def hacker_print(message, text):
    hacker_symbols = ["0", "1", "▓", "▒", "░", "█"]

    try:
        loading_message = await message.reply_text("SYSTEM ACCESS...")
    except:
        return

    async def safe_edit(msg, new_text, parse_html=False):
        try:
            if msg.text == new_text:
                return

            if parse_html:
                await msg.edit_text(new_text, parse_mode="HTML")
            else:
                await msg.edit_text(new_text)

        except BadRequest as e:
            if "Message is not modified" not in str(e):
                raise
        except:
            pass

    for _ in range(3):
        noise = "".join(random.choice(hacker_symbols) for _ in range(30))
        await safe_edit(
            loading_message,
            f"⚡ Запрос принят...\n{noise}"
        )
        await asyncio.sleep(0.4)

    steps = 6
    length = len(text)

    for i in range(1, steps + 1):
        part = text[: int(length * i / steps)]
        await safe_edit(
            loading_message,
            f"🔓 Обращаюсь к серверу расшифровки...\n{part}"
        )
        await asyncio.sleep(0.4)

    await safe_edit(loading_message, text, parse_html=True)


# ---------- START ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    save_user(chat_id)

    # 🌹 Пролог
    await hacker_print(
        update.message,
        "Ciao, amore mio❤️\n\n"
        "✨ Поздравляю тебя с Днём всех сильновлюбленных 🫶\n"
        "И одной самовлюбленной 😏\n"
        "Предлагаю тебе окунуться в его притягательную атмосферу, и начать своё утро чего-то с действительно прекрасного ✨"
    )

    await hacker_print(
        update.message,
        "Если ты готова — следуй подсказкам системы и просто наслаждайся процессом 🖤"
    )

    keyboard = [["💌 Получить наслаждение"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Жду пока ты нажмешь на кнопочку 🌚",
        reply_markup=reply_markup,
    )


# ---------- СПРОСИТЬ ПРО ДЕНЬ ----------
async def ask_day(update: Update):
    keyboard = [
        ["😊 Хороший", "😔 Грустный"],
        ["😩 Тяжёлый", "🤩 Радостный"],
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await hacker_print(update.message, "Как твой день сегодня?")
    await update.message.reply_text(
        "Выбери вариант:",
        reply_markup=reply_markup,
    )


# ---------- ОБРАБОТКА СООБЩЕНИЙ ----------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "💌 Получить наслаждение":
        await update.message.reply_text(
            "⚙️Запуск протокола...",
            reply_markup=ReplyKeyboardRemove(),
        )

        await hacker_print(
            update.message,
            "🛰 Подключение к сердечному ядру...\n"
            "🔐 Доступ подтверждён.\n"
            "⚡ Инициализация режима наслаждения запущена..."
        )

        await hacker_print(
            update.message,
            "Для начала необходимо ответить на один вопрос 💭"
        )

        keyboard = [["Да ❤️", "Очень сильно 💖"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        await update.message.reply_text(
            "Ты меня любишь? 👀",
            reply_markup=reply_markup,
        )

        return

    if text == "Да ❤️":
        await update.message.reply_text(
            "Выбор принят 🖋️",
            reply_markup=ReplyKeyboardRemove(),
        )

        await hacker_print(update.message, "Я тебя тоже ❤️")

        with open("love.png", "rb") as photo:
            await update.message.reply_photo(
                photo=photo,
                caption="Самую прекрасную из 8 миллиардов человек 💕",
            )

        await ask_day(update)

    elif text in ["😊 Хороший", "😔 Грустный", "😩 Тяжёлый", "🤩 Радостный"]:

        # 🔥 УБИРАЕМ КЛАВИАТУРУ НАСТРОЕНИЯ
        await update.message.reply_text(
            "Такс, зафиксировали ✏️",
            reply_markup=ReplyKeyboardRemove(),
        )

        responses = {
            "😊 Хороший": "Значит конечно не до конца идеальный, но я знаю как это исправить 😌",
            "😔 Грустный": "Не знаю, что случилось у моего самого яркого солнца, но я кое-что придумала ☀️",
            "😩 Тяжёлый": "Помни, что я рядом с тобой, несмотря на все невзгоды, и знаю, как тебе помочь 🤍",
            "🤩 Радостный": "Радость – это почти счастье, и я знаю как её повысить ✨",
        }

        await hacker_print(update.message, responses[text])

        keyboard = [
            ["Да 💝"],
            ["⬅ При нажатии кнопки произойдет переобувание 👟🔄👠"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "Хочешь увидеть свой главный подарок? 👀",
            reply_markup=reply_markup,
        )


    elif text == "Очень сильно 💖":
        await update.message.reply_text(
            "Ого 😏",
            reply_markup=ReplyKeyboardRemove(),
        )

        # 📸 Отправляем изображение перед уровнями
        with open("levels_intro.jpg", "rb") as photo:
            await update.message.reply_photo(
                photo=photo,
                caption="Тогда тебя ждёт кое-что особенное… 🌙",
            )

        # 🔘 Кнопка перед уровнями
        keyboard = [["✨ Готова идти дальше"]]
        await hacker_print(
            update.message,
            "⚡ Подготовка следующего этапа...\n🛰 Ожидание подтверждения пользователя"
        )

        await update.message.reply_text(
            "Когда будешь готова — нажми ниже 👇",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
        )


    elif text == "✨ Готова идти дальше":
        await update.message.reply_text(
            "Ниже будет несколько разных цифр, попробуй нажать каждую из них 😎",
            reply_markup=ReplyKeyboardRemove(),
        )

        context.user_data["levels"] = list(range(1, 11))
        context.user_data["after_count"] = 0

        await send_levels(update, context)


    elif text == "Да 💝":
        await update.message.reply_text(
            "Настраиваем сервера шифровок и расшифровок ☎️",
            reply_markup=ReplyKeyboardRemove(),
        )

        await hacker_print(update.message, "Советую не выключать уведомления 🤍")
        await hacker_print(update.message, "С этого момента каждый день для тебя здесь будет кое-что 💌")

        keyboard = [["🔄 Вернуться в начало"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        await update.message.reply_text(
            "Если захочешь пройти всё заново — нажми ниже 👇",
            reply_markup=reply_markup,
        )

        # 🔥 ВОТ ЭТО ДОБАВЬ
        await start_daily_compliments(update, context)



    elif text == "🔄 Вернуться в начало":
        await update.message.reply_text(
            "Давай посмотрим, что ещё тут есть 🔎",
            reply_markup=ReplyKeyboardRemove(),
        )

        await hacker_print(update.message, "❌ Система очищает предыдущий маршрут...")
        await hacker_print(update.message, "✅ Возврат к исходной точке выполнен")

        await start(update, context)

    elif text == "⬅ При нажатии кнопки произойдет переобувание 👟🔄👠":
        await update.message.reply_text(
            "⚙️ Выполняем откат сценария...",
            reply_markup=ReplyKeyboardRemove(),
        )

        await hacker_print(
            update.message,
            "⚠️ Обнаружена попытка экстренного переобувания...\n🔄 Переключение сценария выполнено 😂"
        )

        await ask_day(update)



    elif text == "⏭ SKIP":
        await update.message.reply_text(
            "Пропуск принят 🌙",
            reply_markup=ReplyKeyboardRemove(),
        )

        await hacker_print(update.message, "Грусть, боль, печаль и разочарование 🫠")
        await hacker_print(update.message, "Хоть и не вся любовь раскрыта 😏")
        await hacker_print(update.message, "Доступ к скрытому разделу получен 🔐")

        keyboard = [["Да 💝"]]

        await update.message.reply_text(
            "Хочешь увидеть свой главный подарок? 💌",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
        )


# ---------- INLINE КНОПКИ ----------
async def send_levels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    levels = context.user_data["levels"]
    keyboard = build_keyboard(levels)

    await hacker_print(update.message, "Поехали  🚀")

    # 🔥 Inline с цифрами
    await update.message.reply_text(
        "И так, что же ты выберешь первым 🧐:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

    # 🔥 Обычная кнопка снизу
    reply_keyboard = [["⏭ SKIP"]]
    await update.message.reply_text(
        "Ну или можешь пропустить 👇",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True),
    )


def build_keyboard(levels):
    first_row = [InlineKeyboardButton(str(i), callback_data=str(i)) for i in levels if i <= 5]
    second_row = [InlineKeyboardButton(str(i), callback_data=str(i)) for i in levels if i > 5]

    keyboard = []
    if first_row:
        keyboard.append(first_row)
    if second_row:
        keyboard.append(second_row)

    return keyboard


# ---------- ОБРАБОТКА INLINE ----------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    number = int(query.data)
    levels = context.user_data.get("levels", [])

    if number not in levels:
        return

    # 🌙 БЛОК "ТЫ ВЫБРАЛА"
    await hacker_print(query.message, f"<i>Ты выбрала {number} 🌚</i>")

    responses = {
        1: "<b>Твоя улыбка способна растопить любой мой плохой день 🫶</b>",
        2: "<b>Мне нравится, как ты смеёшься – каждый раз я влюбляюсь в тебя всё сильней 🧡</b>",
        3: "<b>Я люблю в тебе всё – даже то, что ты не можешь не замечать 🧐</b>",
        4: "<b>Для меня ты всегда особенная 🥹</b>",
        5: "<b>В тебе есть глубина, которую хочется узнавать снова и снова 🖤</b>",
        6: "<b>Твой голос – самый приятный звук (особенно его детская версия)💜</b>",
        7: "<b>Ты – моя самая большая радость 👩‍❤️‍👩</b>",
        8: "<b>Ты невероятно талантливая – всё, к чему ты прикасаешься, оживает 🤍</b>",
        9: "<b>Ты – моё любимое уведомление 💌</b>",
        10: "<b>В твоих объятиях я чувствую себя дома 🏠</b>",
    }

    await hacker_print(query.message, responses[number])

    levels.remove(number)
    context.user_data["levels"] = levels

    try:
        await query.edit_message_reply_markup(reply_markup=None)
    except:
        pass

    if levels:
        # 🔥 ДОБАВЛЕН ТВОЙ БЛОК
        after_count = context.user_data.get("after_count", 0) + 1
        context.user_data["after_count"] = after_count

        after_messages = [
            "Тут про тебя 🖤",
            "И тут тоже про тебя 🚀",
            "Чувствую, как ты расплываешься в улыбке 🫶",
            "Остановишься или пойдёшь дальше? 👀",
            "Тут тоже, да, про тебя 🫠",
            "Ага, тоже про тебя 🥹",
            "Неожиданно, но это тоже про тебя 😏",
            "И тут тоже про самую прекрасную девушку в мире🔥",
            "Думала нет? Ни в коем случае, всё еще ты 🤍",
            "Ну еще одну да🤍",
        ]

        message_text = (
            after_messages[after_count - 1]
            if after_count <= len(after_messages)
            else "Ты продолжаешь удивлять 😌"
        )

        await hacker_print(query.message, message_text)

        await query.message.reply_text(
            "Посмотрим, что дальше",
            reply_markup=InlineKeyboardMarkup(build_keyboard(levels)),
        )

    else:
        await hacker_print(query.message, "Все уровни любви раскрыты 🔓")
        await hacker_print(query.message, "Доступ к скрытому разделу получен 🗝")

        keyboard = [["Да 💝"]]

        await query.message.reply_text(
            "Хочешь увидеть свой главный подарок? 💌",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
        )

    # ---------- ЕЖЕДНЕВНЫЕ КОМПЛИМЕНТЫ ----------


async def send_daily_compliment(context: ContextTypes.DEFAULT_TYPE):
    print("🔥 Функция send_daily_compliment вызвана")

    chat_id = context.job.data["chat_id"]

    with open("compliments.json", "r", encoding="utf-8") as f:
        compliments = json.load(f)

    if os.path.exists("progress.json"):
        with open("progress.json", "r") as f:
            progress = json.load(f)
    else:
        progress = {}

    day_index = progress.get(str(chat_id), 0)

    if day_index < len(compliments):
        await context.bot.send_message(
            chat_id=chat_id,
            text=compliments[day_index],
        )

        progress[str(chat_id)] = day_index + 1

        with open("progress.json", "w") as f:
            json.dump(progress, f)

        print("✅ Комплимент отправлен:", day_index)


async def start_daily_compliments(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    if context.job_queue is None:
        print("❌ JobQueue не активен!")
        return

    # удаляем старые задачи
    for job in context.job_queue.get_jobs_by_name(str(chat_id)):
        job.schedule_removal()

    # сообщение о старте
    await context.bot.send_message(
        chat_id=chat_id,
        text="💌 С этого момента начинается твоя ежедневная порция любви..."
    )

    # регистрируем ежедневную задачу
    context.job_queue.run_daily(
        send_daily_compliment,
        time=time(hour=16, minute=55, tzinfo=ZoneInfo("Europe/Moscow")),
        data={"chat_id": chat_id},
        name=str(chat_id),
    )

    print("🕒 Ежедневная задача зарегистрирована для:", chat_id)



# ---------- ЗАПУСК ----------

async def main():
    print("Бот запущен...")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_handler))

    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
