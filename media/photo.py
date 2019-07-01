from logs import logger
from telegram.ext import ConversationHandler


def user_photo(bot, update, user_data):
    photo_id = update.message.photo[-1].file_id
    photo = bot.get_file(photo_id)
    photo.download(f"static/{photo_id}.jpg")
    bot.send_photo(chat_id=update.message.chat.id, photo=open(f"static/{photo_id}.jpg", "rb"))
    return ConversationHandler.END

