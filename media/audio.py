from telegram.ext import ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import data
logger = data.logger


def user_audio(bot, update, user_data):
    audio_id = update.message.audio.file_id
    logger.info(f'Stage: Received an audio file. ID: {audio_id}')
    audio = bot.get_file(audio_id)
    audio.download(f"static/{audio_id}.jpg")
    bot.send_audio(chat_id=update.message.chat.id, audio=open(f"static/{audio_id}.jpg", "rb"))
    bot.deleteMessage(chat_id=update.message.chat_id, message_id=user_data.pop('m_i'))
    reply = InlineKeyboardMarkup([[InlineKeyboardButton(text='Back', callback_data=data.cbMediaOp)]])
    bot.sendMessage(text=f'Success!', reply_markup=reply, chat_id=update.message.chat_id)
    return ConversationHandler.END
