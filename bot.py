from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, RegexHandler, \
    MessageHandler, Filters, PreCheckoutQueryHandler, ShippingQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from handlers import regex_handler, add_subject, edit_subject, callback, clear_messages, oop_search, user_location
from media import user_photo, user_file, user_sticker, user_audio, user_video, user_animation
import data
import payments

logger = data.logger


def start_bot(bot, update):
    markup = [
        [InlineKeyboardButton(text='Show subjects', callback_data=data.cbSubj)],
        [InlineKeyboardButton(text='View schedule', callback_data=data.cbSch)],
        [InlineKeyboardButton(text='Media operations', callback_data=data.cbMediaOp)],
        [InlineKeyboardButton(text='Documents', callback_data=data.cbDocMenu)],
        [InlineKeyboardButton(text='Location', callback_data=data.cbSlocation)]
    ]
    reply = InlineKeyboardMarkup(markup)
    update.message.reply_text(data.hello(update.message.chat.first_name, bot.first_name), reply_markup=reply)


def main():
    upd = Updater(data.settings.API_TOKEN)
    upd.dispatcher.add_handler(CommandHandler('start', start_bot))
    upd.dispatcher.add_handler(CommandHandler('clear', clear_messages))
    upd.dispatcher.add_handler(CommandHandler('noshipping', payments.noshipping))
    upd.dispatcher.add_handler(CommandHandler('shipping', payments.shipping))
    upd.dispatcher.add_handler(ShippingQueryHandler(payments.shipping_callback))
    upd.dispatcher.add_handler(PreCheckoutQueryHandler(payments.precheckout_callback))
    upd.dispatcher.add_handler(MessageHandler(Filters.successful_payment, payments.successful_payment_message))
    upd.dispatcher.add_handler(ConversationHandler(entry_points=[CallbackQueryHandler(callback, pass_user_data=True)],
                                                   states={
                                                       'sched_add_regex': [RegexHandler('^([1-9]|10)$',
                                                                                        regex_handler,
                                                                                        pass_groups=True,
                                                                                        pass_user_data=True)],
                                                       'add_subject': [MessageHandler(Filters.text,
                                                                                      add_subject,
                                                                                      pass_user_data=True)],
                                                       'edit_subject': [MessageHandler(Filters.text,
                                                                                       edit_subject,
                                                                                       pass_user_data=True)],
                                                       'photo': [MessageHandler(Filters.photo,
                                                                                user_photo, pass_user_data=True)],
                                                       'file': [MessageHandler(Filters.document,
                                                                               user_file, pass_user_data=True)],
                                                       'sticker': [MessageHandler(Filters.sticker,
                                                                                  user_sticker, pass_user_data=True)],
                                                       'audio': [MessageHandler(Filters.audio,
                                                                                user_audio, pass_user_data=True)],
                                                       'video': [MessageHandler(Filters.video,
                                                                                user_video, pass_user_data=True)],
                                                       'animation': [MessageHandler(Filters.animation,
                                                                                    user_animation,
                                                                                    pass_user_data=True)],
                                                       'oop_search': [MessageHandler(Filters.text,
                                                                                     oop_search, pass_user_data=True)],
                                                       'location': [MessageHandler(Filters.location,
                                                                                   user_location, pass_user_data=True)]
                                                   },
                                                   fallbacks=[CallbackQueryHandler(callback, pass_user_data=True)]))
    upd.start_polling()
    upd.idle()


if __name__ == '__main__':
    logger = data.logger
    logger.info('Bot started')
    main()
