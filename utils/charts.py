from schemas.currency import Currency
from services.UserStorageManager import UserStorageManager


async def get_portfolio_chart_data(user_id: int, portfolio_name: str, portfolio_id: int, currency: Currency) -> dict:
    chart_data = await UserStorageManager(user_id=user_id).get_chart_data(
        portfolio_id=portfolio_id,
        currency=currency
    )
    time_data = list(map(lambda item: item[1], chart_data))
    value_data = list(map(lambda item: item[0], chart_data))

    result_data = dict(time=time_data,
                       value=value_data,
                       line=[portfolio_name] * len(value_data))

    return result_data
