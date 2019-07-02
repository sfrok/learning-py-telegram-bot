from logs import logger
from telegram.ext import ConversationHandler


def user_file(bot, update):
    file_id = update.message.document.file_id
    file_name = update.message.document.file_name
    file = bot.get_file(file_id)
    file.download(f"static/{file_name}")
    bot.send_document(chat_id=update.message.chat.id, document=open(f"static/{file_name}", "rb"))
    return ConversationHandler.END

