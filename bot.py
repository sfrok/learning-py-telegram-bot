from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import settings


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



#Временный генератор списка предметов
def get_list():
    lst = [
        "Физкультура",
        "Высшая физкультура",
        "Физкультурный анализ"
    ]
    return lst

#Отображение списка WIP
def display_list(bot, update):
    query = update.callback_query
    if query.data == "2":
        tmp = get_list()
        txt = ""
        for i in tmp: 
            txt += "\n" + i
        bot.edit_message_text(text=("Here's the list of available subjects:{}".format(txt)), chat_id=query.message.chat_id, message_id=query.message.message_id)


def main():
    upd = Updater(settings.API_TOKEN)
    upd.dispatcher.add_handler(CommandHandler('start', start_bot))
    upd.dispatcher.add_handler(CallbackQueryHandler(display_list))
    upd.start_polling()
    upd.idle()


if __name__ == '__main__':
    main()