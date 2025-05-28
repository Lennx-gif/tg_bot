### course_bot/config.py

BOT_TOKEN = "7681270870:AAH2qNcU2DJinKn8Vphstp4xEBIV5Z7bl6M"
ADMIN_USERNAME = "@Xenos56make"
COURSE_DIRECTORY = "C:\Windows.old\Users\ADMIN\Desktop\it\Series"
GOOGLE_SHEET_NAME = "Tg_Bot_User_Data"
CREDENTIALS_FILE = "tg_Bot.json"


### course_bot/bot.py

from telegram.ext import Application
from handlers import setup_handlers


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    setup_handlers(app)
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()


### course_bot/handlers.py

from telegram.ext import CommandHandler, MessageHandler, filters, CallbackContext
from telegram import Update
from search import search_local_courses
from download import send_course
from auth import is_authenticated
from storage import log_user_activity


user_data = {}  # In-memory user cache (can be moved to DB)

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Welcome to CourseBot! Send the name of the course you're looking for.")

async def handle_message(update: Update, context: CallbackContext):
    user = update.effective_user
    message = update.message.text
    username = user.username or "unknown"
    phone = user_data.get(user.id, {}).get("phone", "unknown")

    if not is_authenticated(username, phone):
        await update.message.reply_text("You are not authenticated. Please contact support.")
        return

    matches = search_local_courses(message, COURSE_DIRECTORY)

    if matches:
        await send_course(matches[0], update)
        log_user_activity([username, phone, message, "SENT"])
    else:
        await update.message.reply_text("Course not found. We’ll notify the admin to look for it manually.")
        log_user_activity([username, phone, message, "NOT FOUND"])

async def set_phone(update: Update, context: CallbackContext):
    user = update.effective_user
    phone = " ".join(context.args)
    user_data[user.id] = {"phone": phone}
    await update.message.reply_text(f"Phone number {phone} registered.")

def setup_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setphone", set_phone))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))


### course_bot/search.py

import os

def search_local_courses(query, base_path="courses/"):
    matches = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if query.lower() in file.lower():
                matches.append(os.path.join(root, file))
    return matches


### course_bot/download.py

from telegram import Update

async def send_course(file_path, update: Update):
    with open(file_path, 'rb') as file:
        await update.message.reply_document(document=file)


### course_bot/auth.py

from storage import fetch_allowed_users

def is_authenticated(username, phone):
    allowed_users = fetch_allowed_users()
    for user in allowed_users:
        if user['username'] == username and user['phone'] == phone:
            return True
    return False


### course_bot/storage.py

import gspread
from oauth2client.service_account import ServiceAccountCredentials


def get_sheet():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
    client = gspread.authorize(creds)
    return client.open(GOOGLE_SHEET_NAME).sheet1

def log_user_activity(data):
    sheet = get_sheet()
    sheet.append_row(data)

def fetch_allowed_users():
    sheet = get_sheet()
    records = sheet.get_all_records()
    return records


### course_bot/requirements.txt
#python-telegram-bot==20.3
#gspread==5.12.0
#oauth2client==4.1.3
