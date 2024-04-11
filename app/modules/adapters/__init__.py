API_RETIRES = 1
API_TIMEOUT = 10.0
LINE_API_URL = 'https://api.line.me'

from app.modules.adapters.line import LineClient


class Adapter:
    line = LineClient
