from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def start_bot(bot, update):
    user_name = update.message.chat.first_name
    bot_name = bot.first_name

    main_menu_markup = [
        [InlineKeyboardButton(text='Show subjects', callback_data='subjects')],
        [InlineKeyboardButton(text='View schedule', callback_data='schedule')]
    ]

    reply_main_menu = InlineKeyboardMarkup(main_menu_markup)
    update.message.reply_text(f'''Hello {user_name}!
My name is {bot_name} and I will help you getting track of your study schedule.
''', reply_markup=reply_main_menu)
