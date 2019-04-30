#!/usr/bin/env python3
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import settings
import logs
import json

logger = None

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
    sch = {
        'Monday': [],
        'Tuesday': [],
        'Wednesday': [],
        'Thursday': [],
        'Friday': [],
        'Saturday': [],
        'Sunday': []
    }
    default = {'items': lst, 'sched': sch}  # Setting a default library

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


# Updating JSON data
def set_data(id, data):
    id = str(id)
    logger.info('= = = = = Saving user info... = = = = =')
    logger.info(f'Input user id: {id}')
    with open("db.json", "r", encoding='utf-8') as read_file:  # Reading dictionary from database (JSON file)
        user_info = json.load(read_file)
    user_info.update({id: data})
    with open("db.json", "w", encoding='utf-8') as write_file:
        json.dump(user_info, write_file, ensure_ascii=False)
    logger.info('= = = = = Save completed = = = = =')


def callback(bot, update, user_data):

    back_to_main_menu = [
        [InlineKeyboardButton(text='Back', callback_data='back_to_main_menu')],
    ]
    reply = InlineKeyboardMarkup(back_to_main_menu)

    query = update.callback_query
    c_i = query.message.chat_id
    m_i = query.message.message_id

    if query.data == 'subjects':
        user_data['data'] = get_data(query.message.chat_id)  # Requesting schedule data
        tmp = '\n'.join(sorted(user_data['data']['items']))
        logger.info('Subjects list created')
        bot.editMessageText(text=f"Here's the list of available subjects:\n{tmp}",
                            chat_id=c_i, reply_markup=reply, message_id=m_i)
        logger.info('Stage: main menu')
    elif query.data == 'back_to_main_menu':
        logger.info('Stage: Back to main menu')
        user_name = query.message.chat.first_name
        bot_name = bot.first_name
        main_menu_markup = [
            [InlineKeyboardButton(text='Show subjects', callback_data='subjects')],
            [InlineKeyboardButton(text='View schedule', callback_data='schedule')]
        ]
        reply = InlineKeyboardMarkup(main_menu_markup)
        bot.editMessageText(text=f'''Hello {user_name}!
My name is {bot_name} and I will help you getting track of your study schedule.''',
                            chat_id=c_i, reply_markup=reply, message_id=m_i)


    # ------------ Button 'DELETE' in schedule ------------ # START
    elif query.data == 'sched_del_start':
        day = user_data['day']
        user_sched = user_data['data']['sched'][day]
        logger.info('= = = = = DELETING: Deleting an item in schedule... = = = = =')
        logger.info(f'Callback: {query.data}\nDay index: {day}\nSchedule for this day:{user_sched}')
        markup = []
        user_list = user_data['data']['items']
        n = 1
        for j in user_sched:
            if int(j) > int(-1) and int(j) < len(user_list):
                tmp = str(n) + '. ' + user_list[j]
                markup.append([InlineKeyboardButton(text=tmp, callback_data='sched_del_item_'+str(n-1))])
            n += 1
        markup.append([InlineKeyboardButton(text='Delete all', callback_data='sched_del_all')])
        markup.append([InlineKeyboardButton(text='Cancel', callback_data=day)])
        reply = InlineKeyboardMarkup(markup)
        logger.info('= = = = = DELETING: Created a message, waiting for callback = = = = =')
        bot.editMessageText(text='Select what you want to delete:',
                            chat_id=c_i, reply_markup=reply, message_id=m_i)

    elif query.data[:15] == 'sched_del_item_':
        item_id = int(query.data[15:])
        day = user_data['day']
        logger.info(f'Deleting item #{item_id} in the schedule for this day: {day}')
        user_data['data']['sched'][day][item_id] = -1
        set_data(query.message.chat_id, user_data['data'])
        logger.info('= = = = = DELETING: Finished = = = = =')
        update.callback_query.data = day
        callback(bot, update, user_data)

    elif query.data == 'sched_del_all':
        day = user_data['day']
        logger.info(f'Deleting all items in the schedule for this day: {day}')
        user_data['data']['sched'][day] = []
        set_data(query.message.chat_id, user_data['data'])
        logger.info('= = = = = DELETING: Finished = = = = =')
        update.callback_query.data = day
        callback(bot, update, user_data)
    # ------------ Button 'DELETE' in schedule ------------ # END



    else:
        user_data['data'] = get_data(query.message.chat_id)  # Requesting schedule data
        user_sched = user_data['data']['sched']
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        if query.data == 'schedule':
            logger.info('Stage: Showing week days')
            view_schedule = []
            for i in days:
                view_schedule.append([InlineKeyboardButton(text=i, callback_data=i)])
            view_schedule.append([InlineKeyboardButton(text='Back', callback_data='back_to_main_menu')])
            reply = InlineKeyboardMarkup(view_schedule)
            bot.editMessageText(text='Select the day in which you want to view the schedule',
                                chat_id=c_i, reply_markup=reply, message_id=m_i)
        else:
            for i in days:
                if query.data == i:
                    logger.info(f'Stage: Showing schedule for this day: {i}')
                    logger.info(f'------ List of items: {user_sched[i]}')
                    view_schedule = [

                        # add

                    ]

                    # Cleaning up schedule in case it only consists of incorrect ids
                    tmp = 'No lessons yet!'
                    user_list = user_data['data']['items']
                    logger.info(f'------ Length of list of subjects: {len(user_list)}')
                    if user_sched[i] != list([]):
                        empty = True
                        for j in user_sched[i]:
                            if int(j) > int(-1) and int(j) < len(user_list):
                                empty = False
                        if empty:
                            user_data['data']['sched'][i] = []
                            set_data(query.message.chat_id, user_data['data'])

                    if user_sched[i] != list([]):
                        n = 1
                        tmp = f'Schedule for {i}:'
                        for j in user_sched[i]:
                            if int(j) > int(-1) and int(j) < len(user_list):
                                tmp = tmp + ('\n' + str(n) + '. ' + user_list[j])
                            n += 1
                        user_data['day'] = i

                        # edit, delete
                        
                        view_schedule.append([InlineKeyboardButton(text='Delete', callback_data='sched_del_start')])

                    view_schedule.append([InlineKeyboardButton(text='Back', callback_data='back_to_main_menu')])
                    reply = InlineKeyboardMarkup(view_schedule)
                    bot.editMessageText(text=tmp,
                                        chat_id=c_i, reply_markup=reply, message_id=m_i)


def main():
    upd = Updater(settings.API_TOKEN)
    upd.dispatcher.add_handler(CommandHandler('start', start_bot))
    upd.dispatcher.add_handler(CallbackQueryHandler(callback, pass_user_data=True))
    upd.start_polling()
    upd.idle()


if __name__ == '__main__':
    logger = logs.main_logger
    logger.info('Bot started')
    main()
