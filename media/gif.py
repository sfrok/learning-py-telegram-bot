from telegram.ext import ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import data
logger = data.logger


def user_animation(bot, update, user_data):
    animation_id = update.message.animation.file_id
    logger.info(f'Stage: Received an animation file. ID: {animation_id}')
    animation = bot.get_file(animation_id)
    animation.download(f"static/{animation_id}.gif")
    bot.send_animation(chat_id=update.message.chat.id, animation=open(f"static/{animation_id}.gif", "rb"))
    bot.deleteMessage(chat_id=update.message.chat_id, message_id=user_data.pop('m_i'))
    reply = InlineKeyboardMarkup([[InlineKeyboardButton(text='Back', callback_data=data.cbMediaOp)]])
    bot.sendMessage(text=f'Success!', reply_markup=reply, chat_id=update.message.chat_id)
    return ConversationHandler.END
