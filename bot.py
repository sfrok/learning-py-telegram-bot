#!/usr/bin/env python3
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import settings
import logs


def main_menu(user_name, bot_name):
    main_menu_markup = [
        [InlineKeyboardButton(text='Show subjects', callback_data='subjects')],
    ]
    reply_main_menu = InlineKeyboardMarkup(main_menu_markup)
    return [f'''Hello {user_name}.
    My name is {bot_name} and I will help you getting track of your study schedule, 
    right now I know only one command:  /start. ''', reply_main_menu]


def start_bot(bot, update):
    msg = main_menu(update.message.chat.first_name, bot.first_name)
    update.message.reply_text(msg[0], reply_markup=msg[1])


# WIP: replace name subjects [RUS -> ENG]

def get_list():
    lst = [
        'Физкультура',
        'Высшая физкультура',
        'Физкультурный анализ'
    ]
    return sorted(lst)


def callback(bot, update):
    back_to_main_menu = [
        [InlineKeyboardButton(text='Back', callback_data='back_to_main_menu')],
    ]
    reply_back_to_main_menu = InlineKeyboardMarkup(back_to_main_menu)

    query = update.callback_query

    if query.data == 'subjects':
        tmp = '\n'.join(get_list())
        logger.info('Subjects list created')
        bot.sendMessage(text=f"Here's the list of available subjects:\n{tmp}",
                        chat_id=query.message.chat_id,
                        reply_markup=reply_back_to_main_menu)
        logger.info('Stage: main menu')

    if query.data == 'back_to_main_menu':
        logger.info('Stage: Back to main menu')
        msg = main_menu(query.message.chat.first_name, bot.first_name)
        bot.sendMessage(text=msg[0], chat_id=query.message.chat_id, reply_markup=msg[1])


def main():
    upd = Updater(settings.API_TOKEN)
    upd.dispatcher.add_handler(CommandHandler('start', start_bot))
    upd.dispatcher.add_handler(CallbackQueryHandler(callback))
    upd.start_polling()
    upd.idle()


if __name__ == '__main__':
    logger = logs.main_logger
    logger.info('Bot started')
    main()
