import pytest

from services.UserStorageManager import UserStorageManager


@pytest.mark.asyncio
async def test_get_operations(mock_api_handler,
                              mock_user_storage_manager,
                              test_operations):
    storage_manager = UserStorageManager(user_id=1)
    operations = await storage_manager.get_operations()
    assert operations == test_operations


@pytest.mark.asyncio
async def test_update_operation(mock_user_storage_manager,
                                mock_api_handler,
                                test_updated_operation):
    storage_manager = UserStorageManager(user_id=1)
    updated_operation = await storage_manager.update_operation(
        operation_id=1,
        operation=test_updated_operation
    )
    assert updated_operation == test_updated_operation


@pytest.mark.asyncio
async def test_add_operation(mock_user_storage_manager,
                             mock_api_handler,
                             test_operation):
    storage_manager = UserStorageManager(user_id=1)
    operation = await storage_manager.add_operation(test_operation)
    assert operation == test_operation
