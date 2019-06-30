from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import data


def start_bot(bot, update):

    markup = [
        [InlineKeyboardButton(text='Show subjects', callback_data=data.cbSubj)],
        [InlineKeyboardButton(text='View schedule', callback_data=data.cbSch)]
    ]

    reply = InlineKeyboardMarkup(markup)
    update.message.reply_text(data.hello(update.message.chat.first_name, bot.first_name), reply_markup=reply)
