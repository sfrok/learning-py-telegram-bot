import logs
import json


logger = logs.main_logger


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