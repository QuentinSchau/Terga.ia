from flask import Flask
from flask import request
import torch
from src.model.PytorchModel import PytorchModel

app = Flask(__name__)

@app.route("/")
def index():
    return "Index Page"

@app.route("/train/start",methods=['POST'])
def start_train():
    error = None
    if request.method == 'POST':
        net_param = request.get_json()
        if not hasattr(net_param,"model"):
            model = PytorchModel(net_param["model"])
        test = torch.rand(1,10)
        output = model(test)
        print(output)
        # the code below is executed if the request method
        # was GET or the credentials were invalid
    return str(model)
