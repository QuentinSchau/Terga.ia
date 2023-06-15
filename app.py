import os
from multiprocessing import Process
from application import app
from application.model.sse.clientSSE import SSEClient




def behaviorServer():
    if not "MASTERTERGA" in os.environ:
        messages = SSEClient('http://172.31.57.94:5000/listen?name=PC1')
        for msg in messages:
            print(msg)

if __name__ == '__main__':
    p = Process(target=behaviorServer, name="testServeurPL",daemon=True)
    p.start()
    app.run(host="0.0.0.0",port=80,debug=False)
