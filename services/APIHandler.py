import abc
from typing import Type, List, Optional

import aiohttp
from pydantic import BaseModel

from schemas.urls import URLs
from schemas.portfolio import PortfolioSchema
from schemas.state import StateSchema
from schemas.operation import OperationSchema
from schemas.trade import TradeSchema


class AbstractAPIHandler(abc.ABC):

    def __init__(self):
        self.object_url = {
            TradeSchema: URLs.TRADE,
            PortfolioSchema: URLs.PORTFOLIO,
            OperationSchema: URLs.OPERATION,
            StateSchema: URLs.STATE,
        }

    @staticmethod
    async def get_session() -> aiohttp.ClientSession:
        async with aiohttp.ClientSession() as session:
            yield session

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


class APIHandler(AbstractAPIHandler):
    def __init__(self):
        super().__init__()

    async def get_object(self, object_schema: Type[BaseModel], object_id: int) -> Optional[Type[BaseModel]]:
        url = self.object_url[object_schema]
        async with self.get_session() as session:
            async with session.get(url) as resp:
                response_json = await resp.json()
                obj = object_schema(**response_json)
                return obj

    async def post_object(self, object_schema: Type[BaseModel], posting_object: Type[BaseModel]) -> Optional[
        Type[BaseModel]]:
        url = self.object_url[object_schema]
        async with self.get_session() as session:
            async with session.post(url, json=posting_object.model_dump()) as resp:
                response_json = await resp.json()
                obj = object_schema(**response_json)
                return obj

    async def delete_object(self, object_schema: Type[BaseModel], object_id: int):
        url = self.object_url[object_schema]
        async with self.get_session() as session:
            async with session.delete(url + f'/{object_id}') as resp:
                return resp.status

    async def update_object(self, object_schema: Type[BaseModel], object_id: int, updated_object: Type[BaseModel]) -> \
            Optional[Type[BaseModel]]:
        url = self.object_url[object_schema]
        async with self.get_session() as session:
            async with session.put(url + f'/{object_id}', json=updated_object.model_dump()) as resp:
                response_json = await resp.json()
                obj = object_schema(**response_json)
                return obj

    async def object_list(self, object_schema: Type[BaseModel], **kwargs) -> List[Type[BaseModel]]:
        url = self.object_url[object_schema]
        async with self.get_session() as session:
            async with session.get(url, params=kwargs) as resp:
                response_json = await resp.json()
                return list(response_json)
