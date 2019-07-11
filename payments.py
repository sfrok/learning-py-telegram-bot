from telegram import LabeledPrice, ShippingOption
import data

logger = data.logger

# Indexing payment data, NO shipping
NoShID = 'test-payment'  # start_parameter
NoShLp = 'NoShLabeledPrice0'
# Indexing payment data, shipping
ShID = 'test-payment'  # start_parameter
ShLp = 'ShLabeledPrice0'
ShOption = []
ShOption.append('ShOption0Shipping')
ShOption.append('ShOption1Shipping')
ShLpShipping = []
ShLpShipping.append('ShLabeledPrice0Shipping')
ShLpShipping.append('ShLabeledPrice1Shipping')
ShLpShipping.append('ShLabeledPrice2Shipping')
# Indexing payment data, other
ShPL = 'payload1'  # payload
UAH = 'UAH'


def shipping(bot, update):
    chat_id = update.message.chat_id
    title = 'T-shirt'
    payload = ShPL
    description = 'T-shirt with your print'
    start_parameter = ShID
    provider_token = data.settings.PAYMENT_TOKEN
    currency = UAH
    price = 10
    prices = [LabeledPrice(ShLp, price * 100)]
    logger.info(f'Initializing Invoice info: chat_id: {chat_id}, title: {title}, payload: {payload} '
                f'description: {description}, start_parameter: {start_parameter}, currency: {currency}')
    bot.send_invoice(chat_id, title, description, payload, provider_token, start_parameter, currency, prices,
                     need_name=True, need_phone_number=True, need_email=True, need_shippins_address=True,
                     is_flexible=True)


def shipping_callback(bot, update):
    query = update.shipping_query
    logger.info(f'Stage: Callback "shipping_callback", payload: "{query.invoice_payload}"')
    if query.invoice_payload != ShPL:
        bot.answer_shipping_query(shipping_query_id=query.id, ok=False, error_message='Error')
        return
    else:
        options = []
        options.append(ShippingOption(ShOption[0], 'Pickup Post №33', [LabeledPrice(ShLpShipping[0], 100)]))
        price_list = [LabeledPrice(ShLpShipping[1], 150), LabeledPrice(ShLpShipping[2], 200)]
        options.append(ShippingOption(ShOption[1], 'Delivery Post №22', price_list))
        bot.answer_shipping_query(shipping_query_id=query.id, ok=True, shipping_options=options)


def noshipping(bot, update):
    chat_id = update.message.chat_id
    title = 'Edit subject'
    payload = ShPL
    description = 'Unlocks "Edit Subject Function"'
    start_parameter = NoShID
    provider_token = data.settings.PAYMENT_TOKEN
    currency = UAH
    price = 10
    prices = [LabeledPrice(NoShLp, price * 100)]
    logger.info(f'Initializing Invoice info: chat_id: {chat_id}, title: {title}, payload: {payload} '
                f'description: {description}, start_parameter: {start_parameter}, currency: {currency}')
    bot.send_invoice(chat_id, title, description, payload, provider_token, start_parameter, currency, prices)


# The Bot API must receive an answer within 10 seconds after the pre-checkout query was sent.
def precheckout_callback(bot, update):
    query = update.pre_checkout_query
    logger.info(f'Stage: Callback "shipping_callback", payload: "{query.invoice_payload}"')
    if query.invoice_payload != ShPL:
        bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=False, error_message='Error')
    else:
        bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=True)


def successful_payment_message(bot, update):
    logger.info(f'Stage: Payment succsesful')
    update.message.reply_text(f'Thank you, {update.message.chat.first_name}, your purchase was completed!')
