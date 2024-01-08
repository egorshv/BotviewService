import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get("TOKEN")
API_URL = 'http://' + os.environ.get("API_URL")
PORTFOLIO_URL = API_URL + '/portfolio'
STATE_URL = API_URL + '/state'
OPERATION_URL = API_URL + '/operation'
TRADE_URL = API_URL + '/trade'
