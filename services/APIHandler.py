import abc
from typing import Type, List, Optional

import aiohttp
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from schemas.currency import Currency
from schemas.operation import OperationSchema
from schemas.portfolio import PortfolioSchema
from schemas.state import StateSchema
from schemas.trade import TradeSchema
from settings import TRADE_URL, PORTFOLIO_URL, OPERATION_URL, STATE_URL, RECALL_URL, PRECISION_URL, CHART_URL


class AbstractAPIHandler(abc.ABC):

    def __init__(self):
        self.object_url = {
            TradeSchema: TRADE_URL,
            PortfolioSchema: PORTFOLIO_URL,
            OperationSchema: OPERATION_URL,
            StateSchema: STATE_URL,
        }
        self.logical_url = {
            'recall': RECALL_URL,
            'precision': PRECISION_URL,
            'chart': CHART_URL
        }

    @abc.abstractmethod
    async def get_object(self, object_schema: Type[BaseModel], object_id: int) -> Optional[Type[BaseModel]]:
        raise NotImplemented

    @abc.abstractmethod
    async def update_object(self, object_schema: Type[BaseModel], object_id: int, updated_object: Type[BaseModel]) -> \
            Optional[Type[BaseModel]]:
        raise NotImplemented

    @abc.abstractmethod
    async def delete_object(self, object_schema: Type[BaseModel], object_id: int):
        raise NotImplemented

    @abc.abstractmethod
    async def post_object(self, object_schema: Type[BaseModel], posting_object: Type[BaseModel]) -> Optional[
        Type[BaseModel]]:
        raise NotImplemented

    @abc.abstractmethod
    async def object_list(self, object_schema: Type[BaseModel], **kwargs) -> List[Type[BaseModel]]:
        raise NotImplemented

    @abc.abstractmethod
    async def calculate_precision(self, object_schema: Type[BaseModel], portfolio_id: int) -> BaseModel:
        raise NotImplemented

    @abc.abstractmethod
    async def calculate_recall(self, object_schema: Type[BaseModel], portfolio_id: int) -> BaseModel:
        raise NotImplemented

    @abc.abstractmethod
    async def get_chart_data(self, portfolio_id: int, currency: Currency):
        raise NotImplemented


class APIHandler(AbstractAPIHandler):
    def __init__(self):
        super().__init__()

    async def get_object(self, object_schema: Type[BaseModel], object_id: int) -> Optional[BaseModel]:
        url = self.object_url[object_schema]
        async with aiohttp.ClientSession() as session:
            async with session.get(url + f'/{object_id}') as resp:
                response_json = await resp.json()
                obj = object_schema(**response_json)
                return obj

    async def post_object(self, object_schema: Type[BaseModel], posting_object: BaseModel) -> Optional[BaseModel]:
        url = self.object_url[object_schema]
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=jsonable_encoder(posting_object.model_dump())) as resp:
                response_json = await resp.json()
                obj = object_schema(**response_json)
                return obj

    async def delete_object(self, object_schema: Type[BaseModel], object_id: int):
        url = self.object_url[object_schema]
        async with aiohttp.ClientSession() as session:
            async with session.delete(url + f'/{object_id}') as resp:
                return resp.status

    async def update_object(self, object_schema: Type[BaseModel], object_id: int, updated_object: BaseModel) -> \
            Optional[BaseModel]:
        url = self.object_url[object_schema]
        async with aiohttp.ClientSession() as session:
            async with session.put(url + f'/{object_id}', json=jsonable_encoder(updated_object.model_dump())) as resp:
                response_json = await resp.json()
                obj = object_schema(**response_json)
                return obj

    async def object_list(self, object_schema: Type[BaseModel], **kwargs) -> List[BaseModel]:
        url = self.object_url[object_schema]
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=kwargs) as resp:
                response_json = await resp.json()
                return [object_schema(**response) for response in list(response_json)]

    async def calculate_recall(self, object_schema: Type[BaseModel], portfolio_id: int) -> BaseModel:
        url = self.logical_url['recall'].format(portfolio_id)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                response_json = await resp.json()
                return object_schema(**response_json)

    async def calculate_precision(self, object_schema: Type[BaseModel], portfolio_id: int) -> BaseModel:
        url = self.logical_url['precision'].format(portfolio_id)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                response_json = await resp.json()
                return object_schema(**response_json)

    async def get_chart_data(self, portfolio_id: int, currency: Currency):
        url = self.logical_url['chart'].format(portfolio_id)
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params={'currency': currency.value}) as resp:
                response_json = await resp.json()
                return response_json[str(portfolio_id)]
