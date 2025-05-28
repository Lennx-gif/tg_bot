# handlers.py
from turtle import update

def setup_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setphone", set_phone))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

async def course_not_found(update: update):
    await update.message.reply_text("Sorry, course not found. Please describe it, and we'll try to find it manually.")
