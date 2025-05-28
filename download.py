# download.py
from telegram import Update

async def send_course(file_path, update: Update):
    with open(file_path, 'rb') as file:
        await update.message.reply_document(document=file)
