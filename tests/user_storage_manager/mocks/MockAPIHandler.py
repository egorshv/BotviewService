import pytest

from schemas.operation import OperationSchema
from schemas.portfolio import PortfolioSchema
from schemas.state import StateSchema
from schemas.trade import TradeSchema


@pytest.fixture
def mock_api_handler(mocker,
                     test_operation,
                     test_portfolio,
                     test_state,
                     test_trade,
                     test_operations,
                     test_portfolios,
                     test_states,
                     test_trades,
                     test_updated_portfolio,
                     test_updated_operation,
                     test_updated_trade,
                     test_updated_state):
    def mock_init(self):
        self.answer_dict = {
            PortfolioSchema: {
                'obj': test_portfolio,
                'objs': test_portfolios,
                'updated_obj': test_updated_portfolio
            },
            OperationSchema: {
                'obj': test_operation,
                'objs': test_operations,
                'updated_obj': test_updated_operation
            },
            StateSchema: {
                'obj': test_state,
                'objs': test_states,
                'updated_obj': test_updated_state
            },
            TradeSchema: {
                'obj': test_trade,
                'objs': test_trades,
                'updated_obj': test_updated_trade
            },
        }

    async def mock_get_object(self, schema, object_id: int):
        obj = self.answer_dict[schema].get('obj')
        return obj

    async def mock_delete_object(self, schema, object_id: int):
        pass

    async def mock_update_object(self, schema, object_id: int, obj):
        obj = self.answer_dict[schema].get('updated_obj')
        return obj

    async def mock_post_object(self, schema, obj):
        obj = self.answer_dict[schema].get('obj')
        return obj

    async def mock_object_list(self, schema, **kwargs):
        objs = self.answer_dict[schema].get('objs')
        return objs

    mocker.patch('services.APIHandler.APIHandler.__init__', mock_init)
    mocker.patch('services.APIHandler.APIHandler.get_object', mock_get_object)
    mocker.patch('services.APIHandler.APIHandler.post_object', mock_post_object)
    mocker.patch('services.APIHandler.APIHandler.update_object', mock_update_object)
    mocker.patch('services.APIHandler.APIHandler.object_list', mock_object_list)
    mocker.patch('services.APIHandler.APIHandler.delete_object', mock_delete_object)
