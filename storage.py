# storage.py
import gspread,json
from io import StringIO
from oauth2client.service_account import ServiceAccountCredentials

def log_user_activity(data):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials_json = os.getenv("tg_Bot_JSON")
    creds_dict = json.load(StringIO(credentials_json))
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    
    sheet = client.open("Tg_Bot_User_Data").sheet1
    sheet.append_row(data)
