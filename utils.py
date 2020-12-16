from datetime import datetime
from decimal import Decimal

from pycbrf.toolbox import ExchangeRates
from pytz import timezone


def localize(d: datetime) -> datetime:
    return timezone('Europe/Moscow').localize(d)


def get_now() -> datetime:
    return localize(datetime.now())


def get_usd_course() -> Decimal:
    rates = ExchangeRates(get_now().strftime("%Y-%m-%d"))
    return rates['USD'].value

