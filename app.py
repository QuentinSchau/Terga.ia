from multiprocessing import Process
import os
from application import app, tergaClient

if __name__ == '__main__':
    if not "MASTERTERGA" in os.environ:
        tergaClient.name="testClient"
        tergaClient.masterAddress='http://172.31.57.94:5000/'
        p = Process(target=tergaClient.subscrib, name=tergaClient.name, daemon=False)
        p.start()

    app.run(host="0.0.0.0",port=1234,debug=False)
