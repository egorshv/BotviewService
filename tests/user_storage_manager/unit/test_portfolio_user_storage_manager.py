import pytest

from services.UserStorageManager import UserStorageManager


@pytest.mark.asyncio
async def test_get_portfolios(mock_user_storage_manager,
                              mock_api_handler,
                              test_portfolios):
    storage_manager = UserStorageManager(user_id=1)
    portfolios = await storage_manager.get_portfolios()
    assert portfolios == test_portfolios


@pytest.mark.asyncio
async def test_get_portfolio(mock_user_storage_manager,
                             mock_api_handler,
                             test_portfolio):
    storage_manager = UserStorageManager(user_id=1)
    portfolio = await storage_manager.get_portfolio(
        portfolio_id=1
    )
    assert portfolio == test_portfolio


@pytest.mark.asyncio
async def test_update_portfolio(mock_user_storage_manager,
                                mock_api_handler,
                                test_updated_portfolio):
    storage_manager = UserStorageManager(user_id=1)
    updated_portfolio = await storage_manager.update_portfolio(
        portfolio_id=1,
        portfolio=test_updated_portfolio
    )
    assert updated_portfolio == test_updated_portfolio


@pytest.mark.asyncio
async def test_add_portfolio(mock_user_storage_manager,
                             mock_api_handler,
                             test_portfolio):
    storage_manager = UserStorageManager(user_id=1)
    portfolio = await storage_manager.add_portfolio(test_portfolio)
    assert portfolio == test_portfolio
