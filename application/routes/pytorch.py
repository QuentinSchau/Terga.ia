from flask import request
from application import app,tergaClient
from application.auth import token_required, admin_required
from application.model.databaseModel.User import User


@app.route("/train/start",methods=['POST'])
@admin_required
def start_train(user: User):
    if request.method == 'POST':
        net_param = request.get_json()
        tergaClient.runTrain(user.id,net_param)
    return "train"

@app.route("/train/callbacks",methods=['POST'])
@token_required
def setCallbacks():
    if request.method == 'POST':
        callBacksParam = request.get_json()
        tergaClient.setCallbacks(callBacksParam)
    return "set callbacks"

@app.route("/train/logger",methods=['POST'])
@token_required
def setLogger():
    if request.method == 'POST':
        loggerParam = request.get_json()
        tergaClient.setLogger(loggerParam)
    return "set logger"

@app.route("/train/trainer",methods=['POST'])
@token_required
def setTrainer():
    if request.method == 'POST':
        trainerParam = request.get_json()
        tergaClient.setTrainer(trainerParam)
    return "set trainer"

