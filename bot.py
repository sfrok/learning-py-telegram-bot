from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, RegexHandler, \
    MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from handlers import regex_handler, add_subject, edit_subject, callback
import data
logger = data.logger


def start_bot(bot, update):

    markup = [
        [InlineKeyboardButton(text='Show subjects', callback_data=data.cbSubj)],
        [InlineKeyboardButton(text='View schedule', callback_data=data.cbSch)]
    ]

    reply = InlineKeyboardMarkup(markup)
    update.message.reply_text(data.hello(update.message.chat.first_name, bot.first_name), reply_markup=reply)


def main():
    upd = Updater(data.settings.API_TOKEN)
    upd.dispatcher.add_handler(CommandHandler('start', start_bot))
    upd.dispatcher.add_handler(ConversationHandler(entry_points=[CallbackQueryHandler(callback, pass_user_data=True)],
                                                   states={'sched_add_regex': [
                                                       RegexHandler('^([1-9]|10)$', regex_handler, pass_groups=True,
                                                                    pass_user_data=True)],
                                                       'add_subject': [MessageHandler(Filters.text, add_subject,
                                                                                      pass_user_data=True)],
                                                       'edit_subject': [MessageHandler(Filters.text, edit_subject,
                                                                                       pass_user_data=True)]},
                                                   fallbacks=[CallbackQueryHandler(callback, pass_user_data=True)]))
    upd.start_polling()
    upd.idle()


if __name__ == '__main__':
    logger = data.logger
    logger.info('Bot started')
    main()
