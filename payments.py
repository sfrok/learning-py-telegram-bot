from telegram import LabeledPrice, ShippingOption
import settings
import logs

logger = logs.logger


def payment_shipping(bot, update):
    chat_id = update.message.chat_id
    title = 'T-shirt with print'
    payload = 'payment in process'
    description = 'T-shirt with your print'
    start_parameter = 'test-payment'
    provider_token = settings.PAYMENT_TOKEN
    currency = 'UAH'
    price = 10
    prices = [LabeledPrice('test', price * 100)]
    logger.info(f'Initializing Invoice info: chat_id: {chat_id}, title: {title}, payload: {payload} '
                f'description: {description}, start_parameter: {start_parameter}, currency: {currency}')
    bot.send_invoice(chat_id, title, description, payload, provider_token, start_parameter, currency, prices,
                     need_name=True, need_phone_number=True, need_email=True, need_shippins_address=True,
                     is_flexible=True)


def payment_noshipping(bot, update):
    chat_id = update.message.chat_id
    title = 'Edit subject'
    payload = 'payment in process'
    description = 'This function will be to use button of edit subject in you list'
    start_parameter = 'test-payment'
    provider_token = settings.PAYMENT_TOKEN
    currency = 'UAH'
    price = 10
    prices = [LabeledPrice('test', price * 100)]
    logger.info(f'Initializing Invoice info: chat_id: {chat_id}, title: {title}, payload: {payload} '
                f'description: {description}, start_parameter: {start_parameter}, currency: {currency}')
    bot.send_invoice(chat_id, title, description, payload, provider_token, start_parameter, currency, prices)


def shipping_callback(bot, update):
    query = update.shipping_query
    logger.info(f'Information of Callback "{query}"')
    if query.invoice_payload != 'payment in process':
        bot.answer_shipping_query(shipping_query_id=query.id, ok=False, error_message='Error')
        return
    else:
        options = list()
        # a single LabeledPrice
        options.append(ShippingOption('post_1', 'Pickup Post №33', [LabeledPrice('Pickup in UA', 100)]))

        # an array of LabeledPrice objects
        price_list = [LabeledPrice('Box of product', 150), LabeledPrice('Fast delivery (1-2 days) in UA', 200)]
        options.append(ShippingOption('post_2', 'Delivery Post №22', price_list))
        bot.answer_shipping_query(shipping_query_id=query.id, ok=True, shipping_options=options)


# The Bot API must receive an answer within 10 seconds after the pre-checkout query was sent.
def precheckout_callback(bot, update):
    query = update.pre_checkout_query
    logger.info(f'Information of Callback "{query}"')
    if query.invoice_payload != 'payment in process':
        bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=False, error_message='Error')
    else:
        bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=True)


def successful_payment_message(bot, update):
    update.message.reply_text(f'Thank you, {update.message.chat.first_name} your purchase was completed!')
