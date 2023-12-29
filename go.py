from datetime import datetime
from decimal import Decimal
import locale
import os

from dotenv import load_dotenv
from tinkoffapi import TinkoffApi


load_dotenv()

# Токен Тиньков Инвестиций
TOKEN = os.getenv('TINKOFF_TOKEN')
# Идентификатор портфеля в Тиньков инвестициях, его можно получить так:
# tinvest.UserApi(client).accounts_get().parse_json().payload
BROKER_ACCOUNT_ID = os.getenv('TINKOFF_BROKER_ACCOUNT')
# Дата, от которой будут получены пополнения портфеля
BROKER_ACCOUNT_STARTED_AT = datetime.strptime(os.getenv('TINKOFF_ACCOUNT_STARTED'),
                                              '%d.%m.%Y')

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
api = TinkoffApi(api_token=TOKEN, broker_account_id=BROKER_ACCOUNT_ID)
usd_course = api.get_usd_course()
print(f"Текущий курс доллара в брокере: {usd_course} руб")


def get_portfolio_sum() -> int:
    """Возвращает текущую стоимость портфеля в рублях без учета
    просто лежащих на аккаунте рублей в деньгах"""
    positions = api.get_portfolio_positions()

    portfolio_sum = Decimal('0')
    for position in positions:
        current_ticker_cost = (Decimal(str(position.balance))
            * Decimal(str(position.average_position_price.value))
            + Decimal(str(position.expected_yield.value)))
        if position.average_position_price.currency.name == "usd":
            current_ticker_cost *= usd_course
        portfolio_sum += current_ticker_cost
    return int(portfolio_sum)


def get_sum_pay_in() -> int:
    """Возвращает сумму всех пополнений в рублях"""
    operations = api.get_all_operations(BROKER_ACCOUNT_STARTED_AT)

    sum_pay_in = Decimal('0')
    for operation in operations:
        if operation.operation_type.value == "PayIn":
            sum_pay_in += Decimal(str(operation.payment))
    return int(sum_pay_in)


if __name__ ==  "__main__":
    portfolio_sum = get_portfolio_sum()
    sum_pay_in = get_sum_pay_in()
    profit_in_rub = portfolio_sum - sum_pay_in
    profit_in_percent = 100 * round(profit_in_rub / sum_pay_in, 4)
    print(f"Пополнения: {sum_pay_in:n} руб\n"
          f"Текущая  рублёвая стоимость портфеля: {portfolio_sum:n} руб\n"
          f"Рублёвая прибыль: {profit_in_rub:n} руб ({profit_in_percent:n}%)")
