import os
from multiprocessing import Process
from application import app
from application.model.sse.TergaClient import TergaClient


tergaClient = TergaClient()

if __name__ == '__main__':
    if not "MASTERTERGA" in os.environ:
        tergaClient.name="testServeurPL"
        tergaClient.masterAddress='http://172.31.57.94:5000/'
        tergaClient.subscrib()
        p = Process(target=tergaClient.run, name="testServeurPL",daemon=False)
        p.start()

    app.run(host="0.0.0.0",port=1234,debug=True)
