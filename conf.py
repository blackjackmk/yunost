import gspread
import os
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv('TOKEN')
admin_id = [461964422, 712304626]
insta_log = os.getenv('INSTA_LOG')
insta_pass = os.getenv('INSTA_PASS')

sa = gspread.service_account(filename=".config/gspread/service_account.json")
sh = sa.open("applications")

wks = sh.worksheet("answers")

#list of tg id
global acc
acc = set()

def add_user(id):
    with open("users_id.txt", "r") as existed:
        for line in existed:
            line = line.strip()
            acc.add(int(line))
    existed.close()
    acc.add(id)
    with open("users_id.txt", "w") as users_list:
        for user in acc:
            users_list.write(str(user)+"\n")
    users_list.close()




