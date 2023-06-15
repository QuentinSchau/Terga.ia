import queue

class SlaveManager:
    def __init__(self,data: dict):
        self.name = data["name"]
        self.adress = data["adress"]
        self.queueMessage = queue.Queue(maxsize=5)

    def __str__(self):
        return str(dict(name=self.name,adress=self.adress))