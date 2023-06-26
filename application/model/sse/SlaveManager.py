import queue
import json
from flask import request
from lightning.pytorch.loggers import TensorBoardLogger
from lightning.pytorch.callbacks import ModelCheckpoint, LearningRateMonitor
import lightning.pytorch as pl
from multiprocessing import Process
from application import app
from application.model.pytorch.PytorchModel import PytorchModel
from application.model.pytorchLightning.Datamodule import DummyDataModule
from application.model.pytorchLightning.LightningModel import LightningModel

class SlaveManager:
    r"""
    This class implement the slave manager. It control each input and throw error if they are no conform.
    """

    name: str
    ipAddress: str
    queueMessage: queue.Queue
    trainer: pl.Trainer

    def __init__(self,data: dict):
        self.name = data["name"]
        self.ipAddress = data["ipAddress"]
        self.queueMessage = queue.Queue(maxsize=5)
        self.trainer = None

    def getMessage(self):
        """
        Method to get the message from the SSE server.
        TODO Thrown error if the message is not right format
        :return: the current message
        """
        message = self.queueMessage.get()

        return message

    def __str__(self):
        return str(dict(name=self.name,adress=self.ipAddress))

