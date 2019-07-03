from telegram.ext import ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import data

logger = data.logger


def user_scticker(bot, update, user_data):
    sticker_id = update.message.sticker.file_id
    logger.info(f'Stage: Received a sticker. ID: {sticker_id}')
    sticker = bot.get_file(sticker_id)
    sticker.download(f"static/{sticker_id}.jpg")
    bot.send_sticker(chat_id=update.message.chat.id, sticker=open(f"static/{sticker_id}.jpg", "rb"))
    bot.deleteMessage(chat_id=update.message.chat_id, message_id=user_data.pop('m_i'))
    reply = InlineKeyboardMarkup([[InlineKeyboardButton(text='Back', callback_data=data.cbMediaOp)]])
    bot.sendMessage(text=f'Success!', reply_markup=reply, chat_id=update.message.chat_id)
    return ConversationHandler.END
