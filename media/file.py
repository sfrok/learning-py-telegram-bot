from telegram.ext import ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import data
logger = data.logger


def user_file(bot, update, user_data):
    file_id = update.message.document.file_id
    file_name = update.message.document.file_name
    logger.info(f'Stage: Received a file. ID: {file_id}, name: {file_name}')
    file = bot.get_file(file_id)
    file.download(f"static/{file_name}")
    bot.send_document(chat_id=update.message.chat.id, document=open(f"static/{file_name}", "rb"))
    bot.deleteMessage(chat_id=update.message.chat_id, message_id=user_data.pop('m_i'))
    reply = InlineKeyboardMarkup([[InlineKeyboardButton(text='Back', callback_data=data.cbMediaOp)]])
    bot.sendMessage(text=f'Success!', reply_markup=reply, chat_id=update.message.chat_id)
    return ConversationHandler.END

