# config.py

import os

# These values are pulled from environment variables in Render
BOT_TOKEN = os.getenv("7681270870:AAH2qNcU2DJinKn8Vphstp4xEBIV5Z7bl6M")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "@Xenos56make")
COURSE_DIRECTORY = os.getenv("COURSE_DIRECTORY", "https://drive.google.com/drive/folders/1glGJ7ezL1DiLUGxy4bu4tOz-FmQSGleH?usp=sharing")
GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "Tg_Bot_User_Data")
