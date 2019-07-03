from telegram.ext import ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import data
logger = data.logger


def user_video(bot, update):
    video_id = update.message.video.file_id
    logger.info(f'Stage: Received a video file. ID: {video_id}')
    video = bot.get_file(video_id)
    video.download(f"static/{video_id}.jpg")
    bot.send_video(chat_id=update.message.chat.id, video=open(f"static/{video_id}.jpg", "rb"))
    bot.deleteMessage(chat_id=update.message.chat_id, message_id=user_data.pop('m_i'))
    reply = InlineKeyboardMarkup([[InlineKeyboardButton(text='Back', callback_data=data.cbMediaOp)]])
    bot.sendMessage(text=f'Success!', reply_markup=reply, chat_id=update.message.chat_id)
    return ConversationHandler.END
