#!/usr/bin/env python3
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import settings
import logs
import json


def start_bot(bot, update):
    user_name = update.message.chat.first_name
    bot_name = bot.first_name

    main_menu_markup = [
        [InlineKeyboardButton(text='Show subjects', callback_data='subjects')],
        [InlineKeyboardButton(text='View schedule', callback_data='schedule')]
    ]

    reply_main_menu = InlineKeyboardMarkup(main_menu_markup)
    update.message.reply_text(f'''Hello {user_name}!
My name is {bot_name} and I will help you getting track of your study schedule. 
''', reply_markup=reply_main_menu)


# Reading and saving JSON data
def get_data(id):
    id = str(id)
    lst = [
        'Physical Education',
        'Computer architecture',
        'System Programming',
        'Computer networks',
        'Peripherals',
        'Mechanical drawing',
        'Computer circuitry'
    ]
    default = {'items': lst, 'sched': [[], [], [], [], [], [], []]}  # Setting a default library

    logger.info('= = = = = Requesting user info... = = = = =')
    
    with open("db.json", "r", encoding='utf-8') as read_file:  # Reading dictionary from database (JSON file)
        user_info = json.load(read_file)

    logger.info(f'Input user id: {id}')
    logger.info(f'Result (if not found or empty you will see default settings):\n{user_info.get(id, default)}')

    if user_info.get(id, 0) == 0:  # Looking for our user's ID in the dictionary
        user_info.update({id: default})  # If ID is not found, then creating a new entry
        with open("db.json", "w", encoding='utf-8') as write_file:  # Rewriting new data in case of new entry
            json.dump(user_info, write_file, ensure_ascii=False)
        logger.info('Created new entry')

    logger.info('= = = = = Request completed = = = = =')
    return user_info[id]


def callback(bot, update):
    back_to_main_menu = [
        [InlineKeyboardButton(text='Back', callback_data='back_to_main_menu')],
    ]
    reply_back_to_main_menu = InlineKeyboardMarkup(back_to_main_menu)

    query = update.callback_query

    if query.data == 'subjects':
        tmp = '\n'.join(sorted(get_data(query.message.chat_id)["items"]))
        logger.info('Subjects list created')
        bot.editMessageText(text=f"Here's the list of available subjects:\n{tmp}",
                            chat_id=query.message.chat_id,
                            reply_markup=reply_back_to_main_menu,
                            message_id=query.message.message_id
                            )
        logger.info('Stage: main menu')

    elif query.data == 'schedule':
        user_sched = get_data(query.message.chat_id)["sched"]  # Requesting schedule data
        
        view_schedule = [
            [InlineKeyboardButton(text='Monday', callback_data='Monday')],
            [InlineKeyboardButton(text='Tuesday', callback_data='Tuesday')],
            [InlineKeyboardButton(text='Wednesday', callback_data='Wednesday')],
            [InlineKeyboardButton(text='Thursday', callback_data='Thursday')],
            [InlineKeyboardButton(text='Friday', callback_data='Friday')],
            [InlineKeyboardButton(text='Saturday', callback_data='Saturday')],
            [InlineKeyboardButton(text='Sunday', callback_data='Sunday')],
            [InlineKeyboardButton(text='Back', callback_data='back_to_main_menu')]
        ]
        reply_view_schedule = InlineKeyboardMarkup(view_schedule)
        bot.editMessageText(text="Select the day in which you want to view the schedule",
                            chat_id=query.message.chat_id,
                            reply_markup=reply_view_schedule,
                            message_id=query.message.message_id
                            )
    elif query.data == 'back_to_main_menu':
        logger.info('Stage: Back to main menu')
        start_bot(bot, query)


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
