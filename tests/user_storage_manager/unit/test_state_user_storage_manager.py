import pytest

from services.UserStorageManager import UserStorageManager


@pytest.mark.asyncio
async def test_get_states(mock_user_storage_manager,
                          mock_api_handler,
                          test_states):
    storage_manager = UserStorageManager(user_id=1)
    states = await storage_manager.get_states()
    assert states == test_states


@pytest.mark.asyncio
async def test_update_state(mock_user_storage_manager,
                            mock_api_handler,
                            test_updated_state):
    storage_manager = UserStorageManager(user_id=1)
    updated_state = await storage_manager.update_state(
        state_id=1,
        state=test_updated_state
    )
    assert updated_state == test_updated_state


@pytest.mark.asyncio
async def test_add_state(mock_user_storage_manager,
                         mock_api_handler,
                         test_state):
    storage_manager = UserStorageManager(user_id=1)
    state = await storage_manager.add_state(test_state)
    assert state == test_state
