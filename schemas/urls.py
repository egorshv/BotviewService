from enum import Enum


class URLs(str, Enum):
    PORTFOLIO = '/portfolio'
    STATE = '/state'
    OPERATION = '/operation'
    TRADE = '/trade'
