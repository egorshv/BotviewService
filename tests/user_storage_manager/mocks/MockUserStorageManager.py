import pytest

from services.APIHandler import APIHandler


@pytest.fixture
def mock_user_storage_manager(mocker, mock_api_handler):
    def mock_init(self, user_id: int):
        self.user_id = user_id
        self.api_handler = APIHandler()

    mocker.patch("services.UserStorageManager.UserStorageManager.__init__", mock_init)
