
from flask import Flask

from .model.sse.TergaClient import TergaClient

app = Flask(__name__)
tergaClient = TergaClient()
from .routes import index,pytorch,parallelManager


