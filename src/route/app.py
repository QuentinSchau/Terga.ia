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

        model = PytorchModel(net_param)
        test = torch.rand(1,65)
        output = model(test)
        print(output)
        # the code below is executed if the request method
        # was GET or the credentials were invalid
    return
