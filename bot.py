from telegram.ext import Updater, CommandHandler


def start_bot(bot, update):
    hello_var = update.message.chat.first_name
    update.message.reply_text(f'Hello, {hello_var}')


def main(): 
    upd = Updater('TOKEN')
    upd.dispatcher.add_handler(CommandHandler('start', start_bot))
    upd.start_polling()
    upd.idle()


if __name__ == '__main__':
    main()
