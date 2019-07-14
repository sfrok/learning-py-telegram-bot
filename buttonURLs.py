from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import data


def linked_button(function):
    def wrapper(bot, update):
        message_text = 'Enter the any button:'
        markup = [
            [InlineKeyboardButton(text='Go to google.com', url='https://www.google.com/', callback_data=data.cbSite)],
            [InlineKeyboardButton(text='Back', callback_data=data.cbMain)]
        ]
        reply = InlineKeyboardMarkup(markup)
        result = function(bot, update, reply, message_text)
        return result
    return wrapper


@linked_button
def follow_site(bot, update, reply, message_text):
    bot.editMessageText(text=message_text,
                        chat_id=update.callback_query.message.chat_id,
                        reply_markup=reply,
                        message_id=update.callback_query.message.message_id)
