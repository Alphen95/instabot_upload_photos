import glob
import os
import sys
import time
import pathlib
from io import open
from dotenv import load_dotenv
import argparse
from instabot import Bot

def join_image_path(pic_filename):
    pic_name = pic_filename[:-4].split("-")
    return "-".join(pic_name[1:])    

def make_bot(username,password):
    bot = Bot()
    bot.login(username=username, password=password, use_cookie=False)    

if __name__ == "__main__":
    load_dotenv()
    username_instabot = os.getenv("USERNAME_INSTABOT")
    password_instabot = str(os.getenv("PASSWORD_INSTABOT"))
    
    os.chdir(str(pathlib.Path(__file__).parent.absolute()).replace("\\", "/"))
    posted_pic_list = []
    try:
        with open("pics.txt", "r", encoding="utf8") as f:
            posted_pic_list = f.read().splitlines()
    except Exception:
        posted_pic_list = []
    minutes_timeout = 30
    
    parser = argparse.ArgumentParser(
        description='автоматически загружаем фоточки в инстаграм'
    )
    parser.add_argument('--minutes', help='задержка в минутах')
    args = parser.parse_args()
    if args.minutes != None: minutes_timeout = args.minutes
    
    timeout = minutes_timeout * 60
    
    
    while True:
        folder_path = "./images"
        pics = glob.glob(folder_path + "/*.jpg")
        pics = sorted(pics)
        try:
            for pic in pics:
                if pic in posted_pic_list:
                    continue
    
                
    
                print("upload: " + pic_name)
    
                description_file = folder_path + "/" + pic_name + ".txt"
    
                if os.path.isfile(description_file):
                    with open(description_file, "r") as file:
                        caption = file.read()
                else:
                    caption = pic_name.replace("-", " ")
    
                bot.upload_photo(pic, caption=caption)
                if bot.api.last_response.status_code != 200:
                    break
    
                if pic not in posted_pic_list:
                    posted_pic_list.append(pic)
                    with open("pics.txt", "a", encoding="utf8") as f:
                        f.write(pic + "\n")
    
                time.sleep(timeout)
    
        except Exception as e:
            print(str(e))
        time.sleep(60)
