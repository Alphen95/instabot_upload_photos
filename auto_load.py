import glob
import os
import sys
import time
import pathlib
from io import open
from dotenv import load_dotenv
load_dotenv()
username_instabot = os.getenv("USERNAME_INSTABOT")
password_instabot = str(os.getenv("PASSWORD_INSTABOT"))

os.chdir(str(pathlib.Path(__file__).parent.absolute()).replace("\\", "/"))
from instabot import Bot  # noqa: E402

posted_pic_list = []
try:
    with open("pics.txt", "r", encoding="utf8") as f:
        posted_pic_list = f.read().splitlines()
except Exception:
    posted_pic_list = []
second_timeout = 0  # количество секунд при задержке
minutes_timout = 30  # количество минут при задержке
hours_timeout = 0  # количество часов при задержке
timeout = (hours_timeout * 60 * 60) + (minutes_timout * 60) + second_timeout  # таймаут для картинки.

bot = Bot()
bot.login(username=username_instabot, password=password_instabot, use_cookie=False)

while True:
    folder_path = "./images"
    pics = glob.glob(folder_path + "/*.jpg")
    pics = sorted(pics)
    try:
        for pic in pics:
            if pic in posted_pic_list:
                continue

            pic_name = pic[:-4].split("-")
            pic_name = "-".join(pic_name[1:])

            print("upload: " + pic_name)

            description_file = folder_path + "/" + pic_name + ".txt"

            if os.path.isfile(description_file):
                with open(description_file, "r") as file:
                    caption = file.read()
            else:
                caption = pic_name.replace("-", " ")

            bot.upload_photo(pic, caption=caption)
            if bot.api.last_response.status_code != 200:
                print(bot.api.last_response)
                # snd msg
                break

            if pic not in posted_pic_list:
                posted_pic_list.append(pic)
                with open("pics.txt", "a", encoding="utf8") as f:
                    f.write(pic + "\n")

            time.sleep(timeout)

    except Exception as e:
        print(str(e))
    time.sleep(60)