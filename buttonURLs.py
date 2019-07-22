from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import data


def url_reply(bot, update):
    message_text = 'Press any button:'
    markup = [
        [InlineKeyboardButton(text='Go to google.com', url='https://www.google.com/')],
        [InlineKeyboardButton(text='Go to our telegram channel', url='https://t.me/ithumor')],
        [InlineKeyboardButton(text='Go to our telegram king', url='https://t.me/thecete')],
        [InlineKeyboardButton(text='Back', callback_data=data.cbMain)]
    ]
    reply = InlineKeyboardMarkup(markup)
    bot.editMessageText(text=message_text,
                        chat_id=update.callback_query.message.chat_id,
                        reply_markup=reply,
                        message_id=update.callback_query.message.message_id)