from telegram.ext import ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import data
import os
logger = data.logger


def user_audio(bot, update, user_data):
    audio_id = update.message.audio.file_id
    logger.info(f'Stage: Received an audio file. ID: {audio_id}')
    audio = bot.get_file(audio_id)
    my_file = f"static/{audio_id}.mp3"
    audio.download(my_file)
    bot.send_audio(chat_id=update.message.chat.id, audio=open(my_file, "rb"))
    if os.path.isfile(my_file):
        os.remove(my_file)
        logger.info('Removing in static finished')
    else:
        logger.info(f'Error: {my_file} file is not found')
    bot.deleteMessage(chat_id=update.message.chat_id, message_id=user_data.pop('m_i'))
    reply = InlineKeyboardMarkup([[InlineKeyboardButton(text='Back', callback_data=data.cbMediaOp)]])
    bot.sendMessage(text=f'Success!', reply_markup=reply, chat_id=update.message.chat_id)
    return ConversationHandler.END


def user_file(bot, update, user_data):
    file_id = update.message.document.file_id
    file_name = update.message.document.file_name
    logger.info(f'Stage: Received a file. ID: {file_id}, name: {file_name}')
    file = bot.get_file(file_id)
    file.download(f"static/{file_id}/{file_name}")
    bot.send_document(chat_id=update.message.chat.id, document=open(f"static/{file_id}/{file_name}", "rb"))
    my_file = f"static/{file_id}/{file_name}"
    if os.path.isfile(my_file):
        os.remove(my_file)
        logger.info('Removing in static finished')
    else:
        logger.info(f'Error {my_file} file is not found')
    bot.deleteMessage(chat_id=update.message.chat_id, message_id=user_data.pop('m_i'))
    reply = InlineKeyboardMarkup([[InlineKeyboardButton(text='Back', callback_data=data.cbMediaOp)]])
    bot.sendMessage(text=f'Success!', reply_markup=reply, chat_id=update.message.chat_id)
    return ConversationHandler.END


def user_animation(bot, update, user_data):
    logger.info(f'{update.message.animation}')
    gif_id = update.message.animation.file_id
    gif_name = update.message.animation.file_name
    logger.info(f'Stage: Received an animation file. ID: {gif_id}, name: {gif_name}')
    animation = bot.get_file(gif_id)
    animation.download(f"static/{gif_id}.mp4")
    bot.send_animation(chat_id=update.message.chat.id, animation=open(f"static/{gif_id}.mp4", "rb"))
    my_file = f"static/{gif_id}.mp4"
    if os.path.isfile(my_file):
        os.remove(my_file)
        logger.info('Removing in static finished')
    else:
        logger.info(f'Error {my_file} file is not found')
    bot.deleteMessage(chat_id=update.message.chat_id, message_id=user_data.pop('m_i'))
    reply = InlineKeyboardMarkup([[InlineKeyboardButton(text='Back', callback_data=data.cbMediaOp)]])
    bot.sendMessage(text=f'Success!', reply_markup=reply, chat_id=update.message.chat_id)
    return ConversationHandler.END


def user_photo(bot, update, user_data):
    photo_id = update.message.photo[-1].file_id
    logger.info(f'Stage: Received a photo. ID: {photo_id}')
    photo = bot.get_file(photo_id)
    photo.download(f"static/{photo_id}.jpg")
    bot.send_photo(chat_id=update.message.chat.id, photo=open(f"static/{photo_id}.jpg", "rb"))
    my_file = f"static/{photo_id}.jpg"
    if os.path.isfile(my_file):
        os.remove(my_file)
        logger.info('Removing in static finished')
    else:
        logger.info(f'Error {my_file} file is not found')
    bot.deleteMessage(chat_id=update.message.chat_id, message_id=user_data.pop('m_i'))
    reply = InlineKeyboardMarkup([[InlineKeyboardButton(text='Back', callback_data=data.cbMediaOp)]])
    bot.sendMessage(text=f'Success!', reply_markup=reply, chat_id=update.message.chat_id)
    return ConversationHandler.END


def user_sticker(bot, update, user_data):
    sticker_id = update.message.sticker.file_id
    logger.info(f'Stage: Received a sticker. ID: {sticker_id}')
    sticker = bot.get_file(sticker_id)
    sticker.download(f"static/{sticker_id}")
    bot.send_sticker(chat_id=update.message.chat.id, sticker=open(f"static/{sticker_id}", "rb"))
    my_file = f"static/{sticker_id}"
    if os.path.isfile(my_file):
        os.remove(my_file)
        logger.info('Removing in static finished')
    else:
        logger.info(f'Error {my_file} file is not found')
    bot.deleteMessage(chat_id=update.message.chat_id, message_id=user_data.pop('m_i'))
    reply = InlineKeyboardMarkup([[InlineKeyboardButton(text='Back', callback_data=data.cbMediaOp)]])
    bot.sendMessage(text=f'Success!', reply_markup=reply, chat_id=update.message.chat_id)
    return ConversationHandler.END


def user_video(bot, update, user_data):
    logger.info(f'{update.message.animation}')
    video_id = update.message.video.file_id
    logger.info(f'Stage: Received a video file. ID: {video_id}')
    video = bot.get_file(video_id)
    video.download(f"static/{video_id}.mp4")
    bot.send_video(chat_id=update.message.chat.id, video=open(f"static/{video_id}.mp4", "rb"))
    my_file = f"static/{video_id}.mp4"
    if os.path.isfile(my_file):
        os.remove(my_file)
        logger.info('Removing in static finished')
    else:
        logger.info(f'Error {my_file} file is not found')
    bot.deleteMessage(chat_id=update.message.chat_id, message_id=user_data.pop('m_i'))
    reply = InlineKeyboardMarkup([[InlineKeyboardButton(text='Back', callback_data=data.cbMediaOp)]])
    bot.sendMessage(text=f'Success!', reply_markup=reply, chat_id=update.message.chat_id)
    return ConversationHandler.END