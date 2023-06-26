from flask import request
from application import app
global tergaClient

@app.route("/train/start",methods=['POST'])
def start_train():
    if request.method == 'POST':
        net_param = request.get_json()
        tergaClient.runTrain(net_param)
    return "train"

@app.route("/train/callbacks",methods=['POST'])
def setCallbacks():
    if request.method == 'POST':
        callBacksParam = request.get_json()
        tergaClient.setCallbacks(callBacksParam)
    return "set callbacks"

@app.route("/train/logger",methods=['POST'])
def setLogger():
    if request.method == 'POST':
        loggerParam = request.get_json()
        tergaClient.setLogger(loggerParam)
    return "set logger"

@app.route("/train/trainer",methods=['POST'])
def setTrainer():
    if request.method == 'POST':
        trainerParam = request.get_json()
        tergaClient.setTrainer(trainerParam)
    return "set trainer"

