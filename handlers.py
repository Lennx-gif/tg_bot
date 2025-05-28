# handlers.py
from turtle import update


async def course_not_found(update: update):
    await update.message.reply_text("Sorry, course not found. Please describe it, and we'll try to find it manually.")
