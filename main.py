import json
import random
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Загружаем комплименты
with open("compliments.json", "r", encoding="utf-8") as file:
    compliments = json.load(file)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет ❤️ Напиши /compliment, и я скажу что-то приятное.")

# Команда /compliment
async def compliment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    random_compliment = random.choice(compliments)
    await update.message.reply_text(random_compliment)

def main():
    token = os.getenv("BOT_TOKEN")  # токен берётся из переменных окружения

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("compliment", compliment))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
