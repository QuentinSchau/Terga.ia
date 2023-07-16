import flask
import json

import requests
from flask import request
from application import app
from application.auth import token_required, admin_required
from application.model.databaseModel.User import User
from application.model.sse.MasterManager import MasterManager

masterManager = MasterManager()

@app.route('/sent/',methods=['POST'])
@admin_required
def sent(user: User):
    if request.method == 'POST':
        requestBody = request.get_json()
        msg = MasterManager.format_sse(data=requestBody["data"],event=requestBody["event"],user_id=user.id)
        slaveID = None if requestBody['id'] == "all" else int(requestBody['id'])
        masterManager.announce(msg,slaveID)
        return "sent :" + requestBody["event"], 200

@app.route("/list/Slaves",methods=['GET'])
@token_required
def listSlaves():
    return str(masterManager)

@app.route('/listen', methods=['GET'])
def listen():
    if not "name" in request.args : return "missing name args in request",400
    slaveParams = dict(ipAddress=request.remote_addr,name=request.args["name"])
    slave = masterManager.listen(slaveParams)  # returns a queue.Queue

    def stream(slave):
        while True:
            msg = slave.getMessage()  # blocks until a new message arrives
            yield msg

    try : return flask.Response(stream(slave), mimetype='text/event-stream')
    except Exception as e: return flask.Response("error : {0}".format(str(e)),status=403, mimetype='text/event-stream')
