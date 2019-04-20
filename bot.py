from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import settings
import logs


def start_bot(bot, update):
    user_name = update.message.chat.first_name
    bot_name = bot.first_name

    main_menu = [
        [InlineKeyboardButton(text='Show subjects', callback_data='1')],
        ]
    reply_markup = InlineKeyboardMarkup(main_menu)

    update.message.reply_text(f'''Hello {user_name}.
My name is {bot_name} and I will help you getting track of your study schedule, 
right now I know only one command:  /start. ''', reply_markup=reply_markup)


# WID: replace name subjects [RUS -> ENG]

def get_list():
    lst = [
        "Физкультура",
        "Высшая физкультура",
        "Физкультурный анализ"
    ]
    return sorted(lst)


def callback(bot, update):
    query = update.callback_query
    if query.data == "1":
        tmp = '\n'.join(get_list())
        logger.info('List created')
        bot.sendMessage(text=f"Here's the list of available subjects:\n{tmp}",
                        chat_id=query.message.chat_id, message_id=query.message.message_id)
        logger.info('Message send')


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
