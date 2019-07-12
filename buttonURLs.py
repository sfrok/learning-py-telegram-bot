from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import data


def follow_site(bot, update):
    markup = [
        [InlineKeyboardButton(text='Go to google.com', url='https://www.google.com/', callback_data=data.cbSite)],
        [InlineKeyboardButton(text='Back', callback_data=data.cbMain)]
    ]
    reply = InlineKeyboardMarkup(markup)
    bot.editMessageText(text='For following to site, press that button',
                        chat_id=update.callback_query.message.chat_id,
                        reply_markup=reply,
                        message_id=update.callback_query.message.message_id)
