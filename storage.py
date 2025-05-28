# storage.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def log_user_activity(data):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    
    sheet = client.open("CourseBot-Users").sheet1
    sheet.append_row(data)
