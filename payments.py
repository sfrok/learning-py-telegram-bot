from telegram import LabeledPrice, Invoice, ShippingAddress, OrderInfo, ShippingOption, SuccessfulPayment, \
    ShippingQuery, PreCheckoutQuery
import settings


def payment_noshipping(bot, update):
    chat_id = update.message.chat_id
    title = 'Edit subject'
    payload = 'payment in process'
    description = 'This function will be to use button of edit subject in you list'
    start_parameter = 'test-payment'
    provider_token = settings.PAYMENT_TOKEN
    currency = 'UAH'
    price = 50
    prices = [LabeledPrice('test', price * 100)]
    bot.send_invoice(chat_id, title, description, payload, provider_token, start_parameter, currency, prices)


def precheckout_callback(bot, update):
    query = update.pre_checkout_query
    if query.invoice_payload != 'payment in process':
        bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=False, error_message='Something went wrong')
    else:
        bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=True)
        print(update)

# ------------------------------------------------------------------------
# def successful_payment_message(bot, update):
#     update.message.reply_text(f'Thank u {update.message.first_name}')
# ------------------------------------------------------------------------
# THIS WORKING FOR REAL PAYMENT
