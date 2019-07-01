from logs import logger
import settings
import json

# Indexing callback data
cbMain = 'Back to main menu'
cbSubj = 'Showing subject list'
cbSch = 'Showing week days'
cbShare_photo = 'Sharing photo'
cbSch_del1 = 'sched_del_start'
cbSch_del2 = 'sched_del_item_'
cbSch_del3 = 'sched_del_all'
cbSch_add1 = 'sched_add'
cbSch_add2 = 'sched_add_item_'
cbSch_edi1 = 'sched_edit'
cbSch_edi2 = 'sched_edit_subj_'
cbSch_edi3 = 'sched_edit_item_'
cbSubj_del1 = 'subj_del_start'
cbSubj_del2 = 'subj_del_item_'
cbSubj_del3 = 'subj_del_all'
cbSubj_add1 = 'add_subject'
cbSubj_edi1 = 'edit_subject_start'
cbSubj_edi2 = 'edit_subject_item'


def hello(user,
          bot): return f'Hello {user}!\nMy name is {bot} and I will help you getting track of your study schedule.'


# Reading JSON data
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
    lst = sorted(lst)
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

    with open("db.json", "r", encoding='utf-8') as read_file:  # Reading dictionary from database (JSON file)
        user_info = json.load(read_file)

    logger.info(f'get_data(): Input user id: {id}. Result (if n/a you will see default):\n{user_info.get(id, default)}')

    if user_info.get(id, 0) == 0:  # Looking for our user's ID in the dictionary
        user_info.update({id: default})  # If ID is not found, then creating a new entry
        with open("db.json", "w", encoding='utf-8') as write_file:  # Rewriting new data in case of new entry
            json.dump(user_info, write_file, ensure_ascii=False)
        logger.info('get_data(): Created new entry')

    logger.info('get_data(): Finished')
    return user_info[id]


# Updating JSON data
def set_data(id, data):
    id = str(id)
    logger.info(f'set_data(): Input user id: {id}\nset_data(): Info: {data}')
    with open("db.json", "r", encoding='utf-8') as read_file:  # Reading dictionary from database (JSON file)
        user_info = json.load(read_file)
    user_info.update({id: data})
    with open("db.json", "w", encoding='utf-8') as write_file:
        json.dump(user_info, write_file, ensure_ascii=False)
    logger.info('set_data(): Finished')


# Clearing schedule
def sched_clear(sched, items):
    logger.info(f'sched_clear(): Started. Input: {sched}, {items}')
    empty = True
    for j in sched:
        if -1 < int(j) < len(items):
            empty = False
    if empty:
        sched = []
    logger.info(f'sched_clear(): Finished. Result: {sched}')
    return sched