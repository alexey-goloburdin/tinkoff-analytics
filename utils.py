from datetime import datetime
from decimal import Decimal

from pytz import timezone
import tinvest


def localize(d: datetime) -> datetime:
    return timezone('Europe/Moscow').localize(d)


def get_now() -> datetime:
    return localize(datetime.now())


def get_usd_course(client) -> Decimal:
    o = tinvest.MarketApi(client)\
        .market_orderbook_get(figi="BBG0013HGFT4", depth=20)\
        .parse_json().payload
    return Decimal(str(o.last_price))
