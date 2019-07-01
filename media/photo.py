from logs import logger
import os


def user_photo(bot, update, user_data):
    gen = [x for x in range(20)]
    photo = bot.get_file(update.message.photo[-1].file_id)
    list_dir = os.listdir("pyTelegram/static")
    pre_download = photo.download("static/photo_number.jpg")
    for file in list_dir:
        if pre_download == file:

