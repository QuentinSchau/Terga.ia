import flask
import requests
from flask import request
from application import app
from application.model.sse.MasterManager import MasterManager

masterManager = MasterManager()

@app.route('/ping')
def ping():
    msg = MasterManager.format_sse(data='pong',event='add')
    masterManager.announce(msg=msg)
    return "sent", 200

@app.route('/listen', methods=['GET'])
def listen():
    if not "name" in request.args : return "missing name args in request",400
    slaveParams = dict(adress=request.remote_addr,name=request.args["name"])
    slave = masterManager.listen(slaveParams)  # returns a queue.Queue

    def stream(slave):
        while True:
            msg = slave.queueMessage.get()  # blocks until a new message arrives
            yield msg

    return flask.Response(stream(slave), mimetype='text/event-stream')