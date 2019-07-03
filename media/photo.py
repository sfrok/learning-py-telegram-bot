from telegram.ext import ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import data
logger = data.logger


def user_photo(bot, update, user_data):
    photo_id = update.message.photo[-1].file_id
    logger.info(f'Stage: Received a photo. ID: {photo_id}')
    photo = bot.get_file(photo_id)
    photo.download(f"static/{photo_id}.jpg")
    bot.send_photo(chat_id=update.message.chat.id, photo=open(f"static/{photo_id}.jpg", "rb"))
    bot.deleteMessage(chat_id=update.message.chat_id, message_id=user_data.pop('m_i'))
    reply = InlineKeyboardMarkup([[InlineKeyboardButton(text='Back', callback_data=data.cbMediaOp)]])
    bot.sendMessage(text=f'Success!', reply_markup=reply, chat_id=update.message.chat_id)
    return ConversationHandler.END
