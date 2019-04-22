from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import settings
import logs


def start_bot(bot, update):
    user_name = update.message.chat.first_name
    bot_name = bot.first_name

    main_menu = [
        [InlineKeyboardButton(text='Show subjects', callback_data='subjects')],
        [InlineKeyboardButton(text='View schedule', callback_data='schedule')]
    ]
    reply_main_menu = InlineKeyboardMarkup(main_menu)

    update.message.reply_text(f'''Hello {user_name}.
My name is {bot_name} and I will help you getting track of your study schedule,
right now I know only one command:  /start. ''', reply_markup=reply_main_menu)

# WIP: replace name subjects [RUS -> ENG]

def get_list():
    lst = [
        '1.Physical Education',
        '2.Computer architecture',
        '3.System Programming',
        '4.Computer networks',
        '5.Peripherals',
        '6.Mechanical drawing',
        '7.Computer circuitry'
    ]
    return sorted(lst)


def callback(bot, update):

    back_to_main_menu = [
        [InlineKeyboardButton(text='Back', callback_data='back_to_main_menu')],
    ]
    reply_back_to_main_menu = InlineKeyboardMarkup(back_to_main_menu)

    view_schedule = [
        [InlineKeyboardButton(text='Monday', callback_data='Monday')],
        [InlineKeyboardButton(text='Tuesday', callback_data='Tuesday')],
        [InlineKeyboardButton(text='Wednesday', callback_data='Wednesday')],
        [InlineKeyboardButton(text='Thursday', callback_data='Thursday')],
        [InlineKeyboardButton(text='Friday', callback_data='Friday')],
        [InlineKeyboardButton(text='Saturday', callback_data='Saturday')],
        [InlineKeyboardButton(text='Sunday', callback_data='Sunday')]
    ]
    reply_view_schedule = InlineKeyboardMarkup(view_schedule)

    query = update.callback_query

    if query.data == 'subjects':
        tmp = '\n'.join(get_list())
        logger.info('Subjects list created')
        bot.sendMessage(text=f"Here's the list of available subjects:\n{tmp}",
                        chat_id=query.message.chat_id, message_id=query.message.message_id,
                        reply_markup=reply_back_to_main_menu)
        logger.info('Stage: main menu')

    elif query.data == 'schedule':
        bot.sendMessage(text="Select the day in which you want to view the schedule",
                        chat_id=query.message.chat_id, message_id=query.message.message_id,
                        reply_markup=reply_view_schedule)

    if query.data == 'back_to_main_menu':
        logger.info('Stage: Back to main menu')  # WIP -> back to main menu


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
