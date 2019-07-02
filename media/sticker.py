from logs import logger
from telegram.ext import ConversationHandler

def user_scticker(bot, update):
    print(update)
    sticker_id = update.message.sticker.file_id
    sticker = bot.get_file(sticker_id)
    sticker.download(f"static/{sticker_id}.jpg")
    bot.send_sticker(chat_id=update.message.chat.id, sticker=open(f"static/{sticker_id}.jpg", "rb"))
    return ConversationHandler.END
