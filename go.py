import os

from dotenv import load_dotenv
from tinkoff.invest import Client, GetOperationsByCursorRequest, OperationType


load_dotenv()

token = os.environ["TINKOFF_TOKEN"]


def get_sum_pay_in():
    with Client(token) as client:
        accounts = client.users.get_accounts()
        account_id = accounts.accounts[0].id
    
        req = GetOperationsByCursorRequest(
                account_id=account_id,
                operation_types=[OperationType(1)] # only PayIn operations
                )
        operations = client.operations.get_operations_by_cursor(req)

        sum = 0
        for op in operations.items:
            sum += op.payment.units

        return sum


def get_portfolio_sum():
    with Client(token) as client:
        accounts = client.users.get_accounts()
        account_id = accounts.accounts[0].id

        portfolio = client.operations.get_portfolio(account_id=account_id)
        return portfolio.total_amount_portfolio.units


if __name__ ==  "__main__":
    portfolio_sum = get_portfolio_sum()
    sum_pay_in = get_sum_pay_in()

    profit_in_rub = portfolio_sum - sum_pay_in
    profit_in_percent = 100 * round(profit_in_rub / sum_pay_in, 4)

    print(f"Пополнения: {sum_pay_in:n} руб\n"
          f"Текущая  рублёвая стоимость портфеля: {portfolio_sum:n} руб\n"
          f"Рублёвая прибыль: {profit_in_rub:n} руб ({profit_in_percent:n}%)")
