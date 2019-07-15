from telegram.ext import ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import data
import os
logger = data.logger


def media(func):
    def wrapper(bot, update, user_data):
        info = func(bot, update, user_data)
        file_obj = bot.get_file(info[0])
        path = f"static/{info[1]}"
        file_obj.download(path)
        info[2](open(path, "rb"))
        if os.path.isfile(path):
            os.remove(path)
            logger.info('Removing in static finished')
        else:
            logger.info(f'Error: {path} file is not found')
        bot.deleteMessage(chat_id=update.message.chat_id, message_id=user_data.pop('m_i'))
        reply = InlineKeyboardMarkup([[InlineKeyboardButton(text='Back', callback_data=data.cbMediaOp)]])
        bot.sendMessage(text=f'Success!', reply_markup=reply, chat_id=update.message.chat_id)
        return ConversationHandler.END
    return wrapper


@media
def user_audio(bot, update, user_data):
    file_id = update.message.audio.file_id
    logger.info(f'Stage: Received an audio file. ID: {file_id}')
    return [file_id, file_id+'.mp3', lambda f: bot.send_audio(chat_id=update.message.chat.id, audio=f)]


@media
def user_file(bot, update, user_data):
    file_id = update.message.document.file_id
    file_name = update.message.document.file_name
    logger.info(f'Stage: Received a file. ID: {file_id}, name: {file_name}')
    return [file_id, file_id+'/'+file_name, lambda f: bot.send_document(chat_id=update.message.chat.id, document=f)]


@media
def user_animation(bot, update, user_data):
    file_id = update.message.animation.file_id
    file_name = update.message.animation.file_name
    logger.info(f'Stage: Received an animation file. ID: {file_id}, name: {file_name}')
    return [file_id, file_id+'.mp4', lambda f: bot.send_animation(chat_id=update.message.chat.id, animation=f)]


@media
def user_photo(bot, update, user_data):
    file_id = update.message.photo[-1].file_id
    logger.info(f'Stage: Received a photo. ID: {file_id}')
    return [file_id, file_id+'.jpg', lambda f: bot.send_photo(chat_id=update.message.chat.id, photo=f)]


@media
def user_sticker(bot, update, user_data):
    file_id = update.message.sticker.file_id
    logger.info(f'Stage: Received a sticker. ID: {file_id}')
    return [file_id, file_id, lambda f: bot.send_sticker(chat_id=update.message.chat.id, sticker=f)]


@media
def user_video(bot, update, user_data):
    file_id = update.message.file.file_id
    logger.info(f'Stage: Received a video file. ID: {file_id}')
    return [file_id, file_id+'.mp4', lambda f: bot.send_video(chat_id=update.message.chat.id, video=f)]
