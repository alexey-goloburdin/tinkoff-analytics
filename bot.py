import os

from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater
from telegram.ext import CommandHandler

from go import get_portfolio_sum, get_sum_pay_in, api

button = KeyboardButton(text="/info")
custom_keyboard = [[button]]
REPLY_MARKUP = ReplyKeyboardMarkup(custom_keyboard)

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Your telegram account id. It is necessary for the bot to answer only to you
ACCOUNT_ID = os.getenv("ACCOUNT_ID")


def prepare_data() -> str:
    usd_course = api.get_usd_course()
    portfolio_sum = get_portfolio_sum(usd_course)
    sum_pay_in = get_sum_pay_in(usd_course)
    profit_in_rub = portfolio_sum - sum_pay_in
    profit_in_percent = 100 * round(profit_in_rub / sum_pay_in, 4)
    return f"Пополнения: {sum_pay_in:n} руб\n" \
           f"Текущая  рублёвая стоимость портфеля: {portfolio_sum:n} руб\n" \
           f"Рублёвая прибыль: {profit_in_rub:n} руб ({profit_in_percent:n}%)\n" \
           f"Текущий курс доллара в брокере: {usd_course} руб"


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="I will send you info for your investment profit",
                             reply_markup=REPLY_MARKUP)


def send_tags(update, context):
    if update.message.chat.id == int(ACCOUNT_ID):
        text = prepare_data()
    else:
        text = "This is a private bot! You cannot access information from it."
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text, reply_markup=REPLY_MARKUP)


updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
tag_handler = CommandHandler("info", send_tags)
dispatcher.add_handler(tag_handler)

updater.start_polling()
