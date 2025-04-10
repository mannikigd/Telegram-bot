from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Настроение по умолчанию
current_mood = "soft"

# Реплики по настроению
mood_responses = {
    "soft": "мм... спасибо тебе, это очень приятно...",
    "flirty": "ты всегда так со мной заигрываешь? я покраснею...",
    "shy": "я даже не знаю, что сказать... ты заставляешь меня смущаться.",
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет... я здесь. Спасибо, что написал мне.")

async def mood_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_mood
    command = update.message.text.lower().strip("/")
    if command in mood_responses:
        current_mood = command
        await update.message.reply_text(f"Хорошо... теперь я в настроении *{command}*", parse_mode="Markdown")
    else:
        await update.message.reply_text("Я пока не знаю такое настроение...")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply = mood_responses.get(current_mood, "мне нечего сказать...")
    await update.message.reply_text(reply)

if __name__ == '__main__':
    import os

    TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")  # Токен через переменные среды

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("soft", mood_command))
    app.add_handler(CommandHandler("flirty", mood_command))
    app.add_handler(CommandHandler("shy", mood_command))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling()
