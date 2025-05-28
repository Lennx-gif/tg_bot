# handlers.py

from telegram.ext import CommandHandler, MessageHandler, filters, CallbackContext
from telegram import Update
from search import search_local_courses
from download import send_course
from auth import is_authenticated
from storage import log_user_activity
from config import COURSE_DIRECTORY

# In-memory store for user phone numbers
user_data = {}

# /start command handler
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Welcome to CourseBot! Send the name of the course you're looking for."
    )

# /setphone command handler
async def set_phone(update: Update, context: CallbackContext):
    user = update.effective_user
    phone = " ".join(context.args)
    user_data[user.id] = {"phone": phone}
    await update.message.reply_text(f"Phone number {phone} registered.")

# Handler for user messages (course search)
async def handle_message(update: Update, context: CallbackContext):
    user = update.effective_user
    message = update.message.text
    username = user.username or "unknown"
    phone = user_data.get(user.id, {}).get("phone", "unknown")

    if not is_authenticated(username, phone):
        await update.message.reply_text(
            "You are not authenticated. Please contact support."
        )
        return

    matches = search_local_courses(message, COURSE_DIRECTORY)

    if matches:
        await send_course(matches[0], update)
        log_user_activity([username, phone, message, "SENT"])
    else:
        await update.message.reply_text(
            "Course not found. We’ll notify the admin to look for it manually."
        )
        log_user_activity([username, phone, message, "NOT FOUND"])

# This is the function Render needs to import
def setup_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setphone", set_phone))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
