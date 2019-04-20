from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import settings
import logging
import sys


logging.basicConfig(format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
                    stream=sys.stdout,
                    level=logging.INFO,
                    # filename='bot.log',
                    filemode="w"
                    )


def start_bot(bot, update):
    user_name = update.message.chat.first_name
    bot_name = bot.first_name

    main_menu = [
        [InlineKeyboardButton(text='Main Button', callback_data='1')],
        [InlineKeyboardButton(text='Show List', callback_data='2')],
    ]
    reply_markup = InlineKeyboardMarkup(main_menu)

    update.message.reply_text(f'''Hello {user_name}.
My name is {bot_name} and I will help you getting track of your study schedule,
right now I know only one command:  /start.
''', reply_markup=reply_markup)


# Временный генератор списка предметов
def get_list():
    lst = [
        "Физкультура",
        "Высшая физкультура",
        "Физкультурный анализ"
    ]
    return sorted(lst)


def callback(bot, update):
    query = update.callback_query
    if query.data == "2":
        tmp = '\n'.join(get_list())
        logger.info('List create')
        bot.sendMessage(text=f"Here's the list of available subjects:\n{tmp}",
                        chat_id=query.message.chat_id, message_id=query.message.message_id)
        logger.info('Send message')


def main():
    upd = Updater(settings.API_TOKEN)
    upd.dispatcher.add_handler(CommandHandler('start', start_bot))
    upd.dispatcher.add_handler(CallbackQueryHandler(callback))
    upd.start_polling()
    upd.idle()


if __name__ == '__main__':
    logger = logging.getLogger('PythonBot')
    logger.info('Bot started')
    main()
