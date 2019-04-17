from telegram.ext import Updater, CommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import settings


def start_bot(bot, update):
    user_name = update.message.chat.first_name
    bot_name = bot.first_name

    main_menu = [
        [InlineKeyboardButton(text='Main Button', callback_data='1')],
    ]
    reply_markup = InlineKeyboardMarkup(main_menu)

    update.message.reply_text(f'''Hello {user_name}.
My name is {bot_name}, i will to help you track of study schedule,
but now i know only command:  /start. 
''', reply_markup=reply_markup)


def main():
    upd = Updater(settings.API_TOKEN)
    upd.dispatcher.add_handler(CommandHandler('start', start_bot))
    upd.start_polling()
    upd.idle()


if __name__ == '__main__':
    main()
