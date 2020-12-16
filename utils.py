from datetime import datetime
from decimal import Decimal

from pycbrf.toolbox import ExchangeRates
from pytz import timezone


def _get_current_timezone() -> timezone:
    return timezone('Europe/Moscow')


def get_now() -> datetime:
    return _get_current_timezone().localize(datetime.now())


def get_usd_course() -> Decimal:
    rates = ExchangeRates(get_now().strftime("%Y-%m-%d"))
    return rates['USD'].value


def localize(d: datetime) -> datetime:
    return _get_current_timezone().localize(d)
