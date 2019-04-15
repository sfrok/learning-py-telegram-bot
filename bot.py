from telegram.ext import Updater, CommandHandler


def start_bot(bot, update):
    user_name = update.message.chat.first_name
    bot_name = bot.first_name
    update.message.reply_text(f'''Hello {user_name}.
My name is {bot_name}, i will to help you track of study schedule,
but now i know only command:  /start. 
''')


def main(): 
    upd = Updater('TOKEN')
    upd.dispatcher.add_handler(CommandHandler('start', start_bot))
    upd.start_polling()
    upd.idle()


if __name__ == '__main__':
    main()
