import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("tg_Bot.json", scope)
client = gspread.authorize(creds)

sheet = client.open("Tg_Bot_User_Data").sheet1
sheet.append_row(["testuser", "0700000000", "Python Course", "NOTSENT"])

print("Row appended successfully.")
# This script appends a row to a Google Sheet using gspread and OAuth2 credentials.
