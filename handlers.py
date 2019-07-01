from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, RegexHandler, \
    MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import data
logger = data.logger


def regex_handler(bot, update, groups, user_data):
    logger.info(f'Stage: Received regex statement. Regex groups: {groups}')
    bot.deleteMessage(chat_id=update.message.chat_id, message_id=update.message.message_id)
    bot.deleteMessage(chat_id=update.message.chat_id, message_id=user_data['m_i'])
    user_data.pop('m_i')
    user_data['regex'] = groups[0]
    markup = []
    n = 0
    for i in user_data['data']['items']:
        markup.append([InlineKeyboardButton(text=i, callback_data=data.cbSch_add2 + str(n))])
        n += 1
    bot.sendMessage(text=f'You entered {groups[0]}, now select a subject:',
                    reply_markup=InlineKeyboardMarkup(markup), chat_id=update.message.chat_id)
    logger.info(f'Stage: End of regex conversation. Value to pass: {groups[0]}, callback_data: sched_add_item_{i}')
    return ConversationHandler.END


def edit_subject(bot, update, user_data):
    logger.info(f'Stage: Recieved text "{update.message.text}"')
    subjects = user_data['data']['items']
    new_subject_name = update.message.text
    markup = [
        [InlineKeyboardButton(text='Back', callback_data=data.cbMain)]
    ]
    reply = InlineKeyboardMarkup(markup)
    is_clone = False
    query = user_data['update'].callback_query
    old_subject_id = int(query.data[len(data.cbSubj_edi2):])
    for subject in subjects:
        if new_subject_name == subject:
            is_clone = True
            bot.deleteMessage(chat_id=update.message.chat_id, message_id=update.message.message_id)
            bot.editMessageText(text=f'This subject is already in your list, enter another name.',
                                reply_markup=reply, chat_id=update.message.chat_id,
                                message_id=user_data['m_i'])
            return 'edit_subject'
    if not is_clone:
        logger.info(f'Subject to add: {new_subject_name}')
        user_data['data']['items'][old_subject_id] = new_subject_name
        user_data['data']['items'] = sorted(subjects)
        subjects = user_data['data']['items']
        subject_id = subjects.index(new_subject_name)
        sched = user_data['data']['sched'].copy()
        for i in sched:
            logger.info(f'-in cycle. user_data["data"]["sched"][i]: {user_data["data"]["sched"][i]}')
            for j in range(0, len(sched[i])):
                logger.info(f'-in cycle. new_pos: {subject_id}, iter: {sched[i][j]}, '
                            f'old_pos: {old_subject_id}, ')
                if subject_id >= sched[i][j] > old_subject_id:
                    user_data['data']['sched'][i][j] -= 1
                elif subject_id <= sched[i][j] < old_subject_id:
                    user_data['data']['sched'][i][j] += 1
                elif old_subject_id == sched[i][j]:
                    user_data['data']['sched'][i][j] = subject_id
        bot.deleteMessage(chat_id=update.message.chat_id, message_id=update.message.message_id)
        data.set_data(update.message.chat_id, user_data['data'])
        user_data['update'].callback_query.data = data.cbSubj
        callback(bot, user_data.pop('update', 0), user_data)
        logger.info('= = = = = EDITING Subject: FINISHED = = = = =')
    return ConversationHandler.END


def add_subject(bot, update, user_data):
    logger.info(f'Stage: Recieved text "{update.message.text}"')
    subjects = user_data['data']['items']
    subject_name = update.message.text
    markup = [
        [InlineKeyboardButton(text='Back', callback_data=data.cbMain)]
    ]
    reply = InlineKeyboardMarkup(markup)
    is_clone = False
    for subject in subjects:
        if subject_name == subject:
            is_clone = True
            bot.deleteMessage(chat_id=update.message.chat_id, message_id=update.message.message_id)
            bot.editMessageText(text=f'This subject is already in your list, enter another name.',
                                reply_markup=reply, chat_id=update.message.chat_id,
                                message_id=user_data['m_i'])
            return 'add_subject'
    if not is_clone:
        logger.info(f'Subject to add: {subject_name}')
        subjects.append(subject_name)
        user_data["data"]["items"] = sorted(subjects)
        subjects = user_data['data']['items']
        subject_id = subjects.index(subject_name)
        sched = user_data['data']['sched']
        for i in sched:
            for j in range(0, len(sched[i])):
                logger.info(f'-in cycle. item_id: {subject_id}, sched[i][j]: {sched[i][j]}, len(subjects) + 1: '
                            f'{len(subjects) + 1}')
                if len(subjects) + 1 > sched[i][j] >= subject_id:
                    sched[i][j] += 1
            logger.info(f'-in cycle. user_data[data][sched][i]: {user_data["data"]["sched"][i]}')
        logger.info(f'New list of subjects: {subjects}')
        bot.deleteMessage(chat_id=update.message.chat_id, message_id=update.message.message_id)
        data.set_data(update.message.chat_id, user_data['data'])
        user_data['update'].callback_query.data = data.cbSubj
        callback(bot, user_data.pop('update', 0), user_data)
        logger.info('= = = = = ADDING Subject: FINISHED = = = = =')
    return ConversationHandler.END


def callback(bot, update, user_data):
    markup = [[InlineKeyboardButton(text='Back', callback_data=data.cbMain)]]
    reply = InlineKeyboardMarkup(markup)

    query = update.callback_query
    c_i = query.message.chat_id
    m_i = query.message.message_id
    logger.info(f'Stage: Callback "{query.data}"')

    if query.data == data.cbSubj:
        user_data['data'] = data.get_data(query.message.chat_id)  # Requesting schedule data
        markup = [[InlineKeyboardButton(text='Add', callback_data=data.cbSubj_add1)]] + markup
        if user_data['data']['items'] != []:
            tmp = '\n'.join(sorted(user_data['data']['items']))
            markup.insert(1, [InlineKeyboardButton(text='Edit', callback_data=data.cbSubj_edi1)])
            markup.insert(2, [InlineKeyboardButton(text='Delete', callback_data=data.cbSubj_del1)])
            reply = InlineKeyboardMarkup(markup)
            bot.editMessageText(text=f"Here's the list of available subjects:\n{tmp}",
                                chat_id=c_i, reply_markup=reply, message_id=m_i)
        else:
            reply = InlineKeyboardMarkup(markup)
            bot.editMessageText(text="No subjects yet!",
                                chat_id=c_i, reply_markup=reply, message_id=m_i)
            logger.info('Warning - empty subject list!')

    elif query.data == data.cbMain:
        main_menu_markup = [
            [InlineKeyboardButton(text='Show subjects', callback_data=data.cbSubj)],
            [InlineKeyboardButton(text='View schedule', callback_data=data.cbSch)]
        ]
        reply = InlineKeyboardMarkup(main_menu_markup)
        bot.editMessageText(text=data.hello(query.message.chat.first_name, bot.first_name),
                            chat_id=c_i, reply_markup=reply, message_id=m_i)
        return ConversationHandler.END


    # ------------ Button 'DELETE' in schedule ------------ # START
    elif query.data == data.cbSch_del1:
        day = user_data['day']
        sched = user_data['data']['sched'][day]
        logger.info(f'= = = = = DELETING: Deleting an item in schedule for {day}... = = = = =')
        logger.info(f'Schedule for this day: {sched}')
        markup = []
        user_list = user_data['data']['items']
        n = 1
        for j in sched:
            if -1 < int(j) < len(user_list):
                tmp = str(n) + '. ' + user_list[j]
                markup.append([InlineKeyboardButton(text=tmp, callback_data=data.cbSch_del2 + str(n - 1))])
            n += 1
        markup.append([InlineKeyboardButton(text='Delete all', callback_data=data.cbSch_del3)])
        markup.append([InlineKeyboardButton(text='Cancel', callback_data=day)])
        reply = InlineKeyboardMarkup(markup)
        logger.info('= = = = = DELETING: Created a message, waiting for callback = = = = =')
        bot.editMessageText(text='Select what you want to delete:',
                            chat_id=c_i, reply_markup=reply, message_id=m_i)

    elif query.data[:len(data.cbSch_del2)] == data.cbSch_del2:
        item_id = int(query.data[len(data.cbSch_del2):])
        day = user_data['day']
        logger.info(f'Deleting item #{item_id} in the schedule for {day}')
        user_data['data']['sched'][day][item_id] = -1
        user_data['data']['sched'][day] = data.sched_clear(user_data['data']['sched'][day], user_data['data']['items'])
        data.set_data(query.message.chat_id, user_data['data'])
        logger.info('= = = = = DELETING: Finished = = = = =')
        update.callback_query.data = day
        callback(bot, update, user_data)

    elif query.data == data.cbSch_del3:
        day = user_data['day']
        logger.info(f'Deleting all items in the schedule for {day}')
        user_data['data']['sched'][day] = []
        data.set_data(query.message.chat_id, user_data['data'])
        logger.info('= = = = = DELETING: Finished = = = = =')
        update.callback_query.data = day
        callback(bot, update, user_data)
    # ------------ Button 'DELETE' in schedule ------------ # END


    # ------------ Button 'ADD' in schedule ------------ # START
    elif query.data == data.cbSch_add1:
        logger.info('= = = = = ADDING: STARTED = = = = =')
        bot.editMessageText(text='Enter the number of your lesson(1-10)',
                            chat_id=c_i, reply_markup=reply, message_id=m_i)
        logger.info('Stage: Awaiting regex statement')
        user_data['m_i'] = m_i
        return 'sched_add_regex'

    elif query.data[:len(data.cbSch_add2)] == data.cbSch_add2:
        subject_id = int(query.data[len(data.cbSch_add2):])
        lesson_id = int(user_data.pop('regex', '0')) - 1
        logger.info(f'Adding lesson. Lesson id: {lesson_id}, subject id: {subject_id}')
        logger.info(f'Schedule before: {user_data["data"]["sched"][user_data["day"]]}')
        sched = user_data['data']['sched'][user_data['day']]
        if lesson_id < len(sched):
            user_data['data']['sched'][user_data['day']][lesson_id] = subject_id
        else:
            for i in range(len(sched), lesson_id):
                user_data['data']['sched'][user_data['day']].append(-1)
            user_data['data']['sched'][user_data['day']].append(subject_id)
        logger.info(f'Schedule after: {user_data["data"]["sched"][user_data["day"]]}')
        data.set_data(query.message.chat_id, user_data['data'])
        logger.info('= = = = = ADDING: Finished = = = = =')
        update.callback_query.data = user_data['day']
        callback(bot, update, user_data)
    # ------------ Button 'ADD' in schedule ------------ # END


    # ------------ Button 'EDIT' in schedule ------------ # START
    elif query.data == data.cbSch_edi1:
        day = user_data['day']
        sched = user_data['data']['sched'][day]
        subjects = user_data['data']['items']
        logger.info(f'= = = = = EDITING: Editing an item in schedule for {day}... = = = = =')
        logger.info(f'Schedule for this day:{sched}')
        markup = []
        n = 1
        for i in sched:
            if -1 < int(i) < len(subjects):
                subject = str(n) + '. ' + subjects[i]
                markup.append([InlineKeyboardButton(text=subject, callback_data=data.cbSch_edi2 + str(n))])
            n += 1
        markup.append([InlineKeyboardButton(text='Cancel', callback_data=day)])
        reply = InlineKeyboardMarkup(markup)
        bot.editMessageText(text='Enter the number lesson which you want to edit', chat_id=c_i, reply_markup=reply,
                            message_id=m_i)
        logger.info('Created a schedule list, awaiting callback')

    elif query.data[:len(data.cbSch_edi2)] == data.cbSch_edi2:
        user_data['lesson'] = query.data[len(data.cbSch_edi2):]
        markup = []
        n = 0
        for i in user_data['data']['items']:
            markup.append([InlineKeyboardButton(text=i, callback_data=data.cbSch_edi3 + str(n))])
            n += 1
        bot.editMessageText(text=f'You entered {user_data["lesson"]}, now select a subject',
                            reply_markup=InlineKeyboardMarkup(markup), chat_id=c_i, message_id=m_i)
        logger.info('Created a subject list, awaiting callback')

    elif query.data[:len(data.cbSch_edi3)] == data.cbSch_edi3:
        subject_id = int(query.data[len(data.cbSch_edi3):])
        lesson_id = int(user_data.pop('lesson', '0')) - 1
        user_data['data']['sched'][user_data['day']][lesson_id] = subject_id
        data.set_data(query.message.chat_id, user_data['data'])
        logger.info('= = = = = EDITING: Finished = = = = =')
        update.callback_query.data = user_data['day']
        callback(bot, update, user_data)
    # ------------ Button 'EDIT' in schedule ------------ # END


    # ------------ Button 'DELETE' in subjects ------------ # START
    elif query.data == data.cbSubj_del1:
        logger.info('= = = = = DELETING: Deleting a subject... = = = = =')
        markup = []
        n = 0
        for i in user_data['data']['items']:
            markup.append([InlineKeyboardButton(text=i, callback_data=data.cbSubj_del2 + str(n))])
            n += 1
        markup.append([InlineKeyboardButton(text='Delete all', callback_data=data.cbSubj_del3)])
        markup.append([InlineKeyboardButton(text='Cancel', callback_data=data.cbSubj)])
        reply = InlineKeyboardMarkup(markup)
        bot.editMessageText(text='Select what you want to delete:',
                            chat_id=c_i, reply_markup=reply, message_id=m_i)
        logger.info('Created a subject list, awaiting callback')

    elif query.data[:len(data.cbSubj_del2)] == data.cbSubj_del2:
        item_id = int(query.data[len(data.cbSubj_del2):])
        logger.info(f'Deleting item #{item_id} in the subject list')
        sched = user_data['data']['sched']
        subjects = user_data['data']['items']
        subjects.remove(subjects[item_id])
        subjects = sorted(subjects)
        for i in sched:
            logger.info(f'-in cycle. user_data[data][sched][i]: {user_data["data"]["sched"][i]}')
            for j in range(0, len(sched[i])):
                logger.info(f'-in cycle. item_id: {item_id}, sched[i][j]: {sched[i][j]}, len(subjects) + 1: {len(subjects) + 1}')
                if sched[i][j] == item_id:
                    sched[i][j] = -1
                elif len(subjects) + 1 > sched[i][j] > item_id:
                    sched[i][j] -= 1
            user_data['data']['sched'][i] = data.sched_clear(sched[i], subjects)
        user_data['data']['items'] = subjects
        data.set_data(query.message.chat_id, user_data['data'])
        logger.info('= = = = = DELETING: Finished = = = = =')
        update.callback_query.data = data.cbSubj
        callback(bot, update, user_data)

    elif query.data == data.cbSubj_del3:
        logger.info('Deleting all subjects')
        user_data['data']['items'] = []
        for i in user_data['data']['sched']:
            user_data['data']['sched'][i] = []
        data.set_data(query.message.chat_id, user_data['data'])
        logger.info('= = = = = DELETING: Finished = = = = =')
        update.callback_query.data = data.cbSubj
        callback(bot, update, user_data)
    # ------------ Button 'DELETE' in subjects ------------ # END


    # ------------ Button 'ADD' in subjects ------------ # START
    elif query.data == data.cbSubj_add1:
        logger.info('= = = = = ADDING: Adding a subject... = = = = =')
        bot.editMessageText(text='Enter the name of your subject', chat_id=c_i,
                            reply_markup=reply,
                            message_id=m_i)
        user_data['m_i'] = m_i
        user_data['update'] = update
        return 'add_subject'
    # ------------ Button 'ADD' in subjects ------------ # END


    # ------------ Button 'EDIT' in subjects ------------ # START
    elif query.data == data.cbSubj_edi1:
        logger.info('= = = = = EDITING: Editing a subject... = = = = =')
        markup = []
        n = 0
        for i in user_data['data']['items']:
            markup.append([InlineKeyboardButton(text=i, callback_data=data.cbSubj_edi2 + str(n))])
            n += 1
        markup.append([InlineKeyboardButton(text='Cancel', callback_data=data.cbSubj)])
        reply = InlineKeyboardMarkup(markup)
        logger.info('Created a subject list, awaiting callback')
        bot.editMessageText(text='Select what you want to edit:',
                            chat_id=c_i, reply_markup=reply, message_id=m_i)

    elif query.data[:len(data.cbSubj_edi2)] == data.cbSubj_edi2:
        bot.editMessageText(text='Enter the name of your subject', chat_id=c_i,
                            reply_markup=reply,
                            message_id=m_i)
        user_data['m_i'] = m_i
        user_data['update'] = update
        return 'edit_subject'
    # ------------ Button 'EDIT' in subjects ------------ # END


    # ------------ Button 'SHARE PHOTO'  ------------ # START
    elif query.data == data.cbShare_photo:
        logger.info('Created a message, awaiting photo')
        bot.sendMessage(text='Give me your another photo', chat_id=c_i, message_id=m_i)
        return 'photo'
    # ------------ Button 'SHARE PHOTO' ------------ # END


    else:
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        if query.data == data.cbSch:
            view_schedule = []
            for i in days:
                view_schedule.append([InlineKeyboardButton(text=i, callback_data=i)])
            view_schedule.append([InlineKeyboardButton(text='Back', callback_data=data.cbMain)])
            reply = InlineKeyboardMarkup(view_schedule)
            bot.editMessageText(text='Select the day in which you want to view the schedule',
                                chat_id=c_i, reply_markup=reply, message_id=m_i)
        else:
            for i in days:
                if query.data == i:
                    user_data['data'] = data.get_data(query.message.chat_id)  # Requesting schedule data
                    sched = user_data['data']['sched']
                    logger.info(f'List of items: {sched[i]}')
                    user_data['day'] = i
                    view_schedule = [
                        [InlineKeyboardButton(text='Add', callback_data=data.cbSch_add1)]
                    ]
                    # Cleaning up schedule in case it only consists of incorrect ids
                    tmp = 'No lessons yet!'
                    user_list = user_data['data']['items']
                    logger.info(f'Length of list of subjects: {len(user_list)}')
                    if sched[i] != list([]):
                        n = 1
                        tmp = f'Schedule for {i}:'
                        for j in sched[i]:
                            if -1 < int(j) < len(user_list):
                                tmp = tmp + ('\n' + str(n) + '. ' + user_list[j])
                            n += 1
                        view_schedule.append([InlineKeyboardButton(text='Edit', callback_data=data.cbSch_edi1)])
                        view_schedule.append([InlineKeyboardButton(text='Delete', callback_data=data.cbSch_del1)])
                    view_schedule.append([InlineKeyboardButton(text='Back', callback_data=data.cbMain)])
                    reply = InlineKeyboardMarkup(view_schedule)
                    bot.editMessageText(text=tmp,
                                        chat_id=c_i, reply_markup=reply, message_id=m_i)
