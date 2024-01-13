import pytest
from services.UserStorageManager import UserStorageManager


@pytest.mark.asyncio
async def test_get_trades(mock_user_storage_manager,
                          mock_api_handler,
                          test_trades):
    storage_manager = UserStorageManager(user_id=1)
    trades = await storage_manager.get_trades()
    assert trades == test_trades


@pytest.mark.asyncio
async def test_add_trade(mock_user_storage_manager,
                         mock_api_handler,
                         test_trade):
    storage_manager = UserStorageManager(user_id=1)
    trade = await storage_manager.add_trade(test_trade)
    assert trade == test_trade


@pytest.mark.asyncio
async def test_update_trade(mock_user_storage_manager,
                            mock_api_handler,
                            test_updated_trade):
    storage_manager = UserStorageManager(user_id=1)
    trade = await storage_manager.update_trade(
        trade_id=1,
        trade=test_updated_trade
    )
    assert trade == test_updated_trade
