import pytest

from schemas.currency import Currency
from services.UserStorageManager import UserStorageManager


@pytest.mark.asyncio
async def test_get_recall():
    storage_manager = UserStorageManager(user_id=1)
    recall = await storage_manager.calculate_portfolio_recall(5)
    assert recall == 1


@pytest.mark.asyncio
async def test_get_precision():
    storage_manager = UserStorageManager(user_id=1)
    precision = await storage_manager.calculate_portfolio_precision(5)
    assert precision == 1


@pytest.mark.asyncio
async def test_get_chart_data():
    storage_manager = UserStorageManager(user_id=1)
    chart_data = await storage_manager.get_chart_data(3, Currency.RUB)
    assert chart_data
