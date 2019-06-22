from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, RegexHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from greet import start_bot
import settings
import logs
import data


logger = None


def regex_handler(bot, update, groups, user_data):
    logger.info(f'Stage: Received regex statement. Regex groups: {groups}')
    bot.deleteMessage(chat_id=update.message.chat_id, message_id=update.message.message_id)
    bot.deleteMessage(chat_id=update.message.chat_id, message_id=user_data['m_i'])
    user_data.pop('m_i')
    user_data['regex'] = groups[0]
    markup = []
    n = 0
    for i in user_data['data']['items']:
        markup.append([InlineKeyboardButton(text=i, callback_data='sched_add_item_' + str(n))])
        n += 1
    bot.sendMessage(text=f'You entered {groups[0]}, now select a subject:',
                    reply_markup=InlineKeyboardMarkup(markup), chat_id=update.message.chat_id)
    logger.info(f'Stage: End of regex conversation. Value to pass: {groups[0]}, callback_data: sched_add_item_{i}')
    return ConversationHandler.END


def callback(bot, update, user_data):
    back_to_main_menu = [
        [InlineKeyboardButton(text='Back', callback_data='back_to_main_menu')],
    ]
    reply = InlineKeyboardMarkup(back_to_main_menu)

    query = update.callback_query
    c_i = query.message.chat_id
    m_i = query.message.message_id

    if query.data == 'subjects':
        user_data['data'] = data.get_data(query.message.chat_id)  # Requesting schedule data
        if user_data['data']['items'] != []:
            tmp = '\n'.join(sorted(user_data['data']['items']))
            logger.info('Subjects list created')
            markup = [
                [InlineKeyboardButton(text='Delete', callback_data='subj_del_start')],
            ] + back_to_main_menu
            reply = InlineKeyboardMarkup(markup)
            bot.editMessageText(text=f"Here's the list of available subjects:\n{tmp}",
                                chat_id=c_i, reply_markup=reply, message_id=m_i)
            logger.info('Stage: main menu')
        else:
            bot.editMessageText(text="No subjects yet!",
                                chat_id=c_i, reply_markup=reply, message_id=m_i)
        
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
        return ConversationHandler.END


    # ------------ Button 'DELETE' in schedule ------------ # START
    elif query.data == 'sched_del_start':
        day = user_data['day']
        sched = user_data['data']['sched'][day]
        logger.info('= = = = = DELETING: Deleting an item in schedule... = = = = =')
        logger.info(f'Day index: {day}\nSchedule for this day:{sched}')
        markup = []
        user_list = user_data['data']['items']
        n = 1
        for j in sched:
            if -1 < int(j) < len(user_list):
                tmp = str(n) + '. ' + user_list[j]
                markup.append([InlineKeyboardButton(text=tmp, callback_data='sched_del_item_' + str(n - 1))])
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
        logger.info(f'Callback: {query.data}\nDeleting item #{item_id} in the schedule for this day: {day}')
        user_data['data']['sched'][day][item_id] = -1
        user_data['data']['sched'][day] = data.sched_clear(user_data['data']['sched'][day], user_data['data']['items'])
        data.set_data(query.message.chat_id, user_data['data'])
        logger.info('= = = = = DELETING: Finished = = = = =')
        update.callback_query.data = day
        callback(bot, update, user_data)

    elif query.data == 'sched_del_all':
        day = user_data['day']
        logger.info(f'Deleting all items in the schedule for this day: {day}')
        user_data['data']['sched'][day] = []
        data.set_data(query.message.chat_id, user_data['data'])
        logger.info('= = = = = DELETING: Finished = = = = =')
        update.callback_query.data = day
        callback(bot, update, user_data)
    # ------------ Button 'DELETE' in schedule ------------ # END


    # ------------ Button 'ADD' in schedule ------------ # START
    elif query.data == 'sched_add':
        logger.info('= = = = = ADDING: STARTED = = = = =')
        bot.editMessageText(text='Enter the number of your lesson(1-10)',
                            chat_id=c_i, reply_markup=reply, message_id=m_i)
        logger.info('Stage: Awaiting regex statement')
        user_data['m_i'] = m_i
        return 'sched_add_regex'

    elif query.data[:15] == 'sched_add_item_':
        subject_id = int(query.data[15:])
        lesson_id = int(user_data.pop('regex', '0')) - 1
        logger.info(f'Stage: Adding lesson. Lesson id: {lesson_id}, subject id: {subject_id}')
        logger.info(f'Stage: Adding lesson. Schedule before: {user_data["data"]["sched"][user_data["day"]]}')
        sched = user_data['data']['sched'][user_data['day']]
        if lesson_id < len(sched):
            user_data['data']['sched'][user_data['day']][lesson_id] = subject_id
        else:
            for i in range(len(sched), lesson_id):
                user_data['data']['sched'][user_data['day']].append(-1)
            user_data['data']['sched'][user_data['day']].append(subject_id)
        logger.info(f'Stage: Adding lesson. Schedule after: {user_data["data"]["sched"][user_data["day"]]}')
        data.set_data(query.message.chat_id, user_data['data'])
        logger.info('= = = = = ADDING: Finished = = = = =')
        update.callback_query.data = user_data['day']
        callback(bot, update, user_data)
    # ------------ Button 'ADD' in schedule ------------ # END


    # ------------ Button 'EDIT' in schedule ------------ # START
    elif query.data == 'sched_edit':
        day = user_data['day']
        sched = user_data['data']['sched'][day]
        subjects = user_data['data']['items']
        logger.info('= = = = = EDITING: Editing an item in schedule... = = = = =')
        logger.info(f'Callback: {query.data}\nDay index: {day}\nSchedule for this day:{sched}')
        markup = []
        n = 1
        for i in sched:
            if -1 < int(i) < len(subjects):
                subject = str(n) + '. ' + subjects[i]
                markup.append([InlineKeyboardButton(text=subject, callback_data='sched_edit_subj_' + str(n))])
            n += 1
        markup.append([InlineKeyboardButton(text='Cancel', callback_data=day)])
        reply = InlineKeyboardMarkup(markup)
        bot.editMessageText(text='Enter the number lesson which you want to edit', chat_id=c_i, reply_markup=reply,
                            message_id=m_i)
        logger.info('Created a schedule message, awaiting callback')

    elif query.data[:16] == 'sched_edit_subj_':
        user_data['lesson'] = query.data[16:]
        markup = []
        n = 0
        for i in user_data['data']['items']:
            markup.append([InlineKeyboardButton(text=i, callback_data='sched_edit_item_' + str(n))])
            n += 1
        bot.sendMessage(text=f'You entered {user_data["lesson"]}, now select a subject',
                        reply_markup=InlineKeyboardMarkup(markup), chat_id=c_i, message_id=m_i)
        logger.info('Created a subject list, awaiting callback')

    elif query.data[:16] == 'sched_edit_item_':
        subject_id = int(query.data[16:])
        lesson_id = int(user_data.pop('lesson', '0')) - 1
        user_data['data']['sched'][user_data['day']][lesson_id] = subject_id
        data.set_data(query.message.chat_id, user_data['data'])
        logger.info('= = = = = EDITING: Finished = = = = =')
        update.callback_query.data = user_data['day']
        callback(bot, update, user_data)
    # ------------ Button 'EDIT' in schedule ------------ # END


    # ------------ Button 'DELETE' in subjects ------------ # START
    elif query.data == 'subj_del_start':
        logger.info('= = = = = DELETING: Deleting a subject... = = = = =')
        markup = []
        n = 0
        for i in user_data['data']['items']:
            markup.append([InlineKeyboardButton(text=i, callback_data='subj_del_item_' + str(n))])
            n += 1
        markup.append([InlineKeyboardButton(text='Delete all', callback_data='subj_del_all')])
        markup.append([InlineKeyboardButton(text='Cancel', callback_data='subjects')])
        reply = InlineKeyboardMarkup(markup)
        logger.info('= = = = = DELETING: Created a message, waiting for callback = = = = =')
        bot.editMessageText(text='Select what you want to delete:',
                            chat_id=c_i, reply_markup=reply, message_id=m_i)

    elif query.data[:14] == 'subj_del_item_':
        item_id = int(query.data[14:])
        logger.info(f'Callback: {query.data}. Deleting item #{item_id} in the subject list')
        sched = user_data['data']['sched']
        subjects = user_data['data']['items']
        subjects.remove(subjects[item_id])
        subjects = sorted(subjects)
        for i in (sched):
            for j in range (0, len(sched[i])):
                logger.info(f'-in cycle. item_id: {item_id}, sched[i][j]: {sched[i][j]}, len(subjects) + 1: {len(subjects) + 1}')
                if sched[i][j] == item_id:
                    sched[i][j] = -1
                elif len(subjects) + 1 > sched[i][j] > item_id:
                    sched[i][j] -= 1
            user_data['data']['sched'][i] = data.sched_clear(sched[i], subjects)
            logger.info(f'-in cycle. user_data[data][sched][i]: {user_data["data"]["sched"][i]}')
        user_data['data']['items'] = subjects
        data.set_data(query.message.chat_id, user_data['data'])
        logger.info('= = = = = DELETING: Finished = = = = =')
        update.callback_query.data = 'subjects'
        callback(bot, update, user_data)

    elif query.data == 'subj_del_all':
        logger.info('Deleting all subjects')
        user_data['data']['items'] = []
        for i in user_data['data']['sched']:
            user_data['data']['sched'][i] = []
        data.set_data(query.message.chat_id, user_data['data'])
        logger.info('= = = = = DELETING: Finished = = = = =')
        update.callback_query.data = 'subjects'
        callback(bot, update, user_data)
    # ------------ Button 'DELETE' in subjects ------------ # END


    else:
        user_data['data'] = data.get_data(query.message.chat_id)  # Requesting schedule data
        sched = user_data['data']['sched']
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
                    logger.info(f'------ List of items: {sched[i]}')
                    user_data['day'] = i
                    view_schedule = [
                        [InlineKeyboardButton(text='Add', callback_data='sched_add')]
                    ]
                    # Cleaning up schedule in case it only consists of incorrect ids
                    tmp = 'No lessons yet!'
                    user_list = user_data['data']['items']
                    logger.info(f'------ Length of list of subjects: {len(user_list)}')
                    if sched[i] != list([]):
                        n = 1
                        tmp = f'Schedule for {i}:'
                        for j in sched[i]:
                            if -1 < int(j) < len(user_list):
                                tmp = tmp + ('\n' + str(n) + '. ' + user_list[j])
                            n += 1

                        # edit, delete
                        view_schedule.append([InlineKeyboardButton(text='Edit', callback_data='sched_edit')])

                        view_schedule.append([InlineKeyboardButton(text='Delete', callback_data='sched_del_start')])

                    view_schedule.append([InlineKeyboardButton(text='Back', callback_data='back_to_main_menu')])
                    reply = InlineKeyboardMarkup(view_schedule)
                    bot.editMessageText(text=tmp,
                                        chat_id=c_i, reply_markup=reply, message_id=m_i)


def main():
    upd = Updater(settings.API_TOKEN)
    upd.dispatcher.add_handler(CommandHandler('start', start_bot))
    upd.dispatcher.add_handler(ConversationHandler(entry_points=[CallbackQueryHandler(callback, pass_user_data=True)],
                                                   states={'sched_add_regex': [
                                                       RegexHandler('^([1-9]|10)$', regex_handler, pass_groups=True,
                                                                    pass_user_data=True)]},
                                                   fallbacks=[CallbackQueryHandler(callback, pass_user_data=True)]))
    upd.start_polling()
    upd.idle()


if __name__ == '__main__':
    logger = logs.main_logger
    logger.info('Bot started')
    main()
