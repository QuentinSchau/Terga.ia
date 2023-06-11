from flask import Flask
from flask import request
from lightning.pytorch.loggers import TensorBoardLogger
from lightning.pytorch.callbacks import ModelCheckpoint,LearningRateMonitor
from src.model.Datamodule import DummyDataModule
from src.model.LightningModel import LightningModel
import lightning.pytorch as pl
from src.model.PytorchModel import PytorchModel
from multiprocessing import Process
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "Index Page"

@app.route("/train/start",methods=['POST'])
def start_train():
    error = None
    if request.method == 'POST':
        net_param = request.get_json()
        if not hasattr(net_param,"model"):
            model = PytorchModel(net_param["model"])
        else: raise ValueError("model is not defined in the JSON parameters, you should defined it, see the doc")

        dataModule = DummyDataModule(net_param["dataModuleArgs"])
        lightningModel = LightningModel(model,net_param)

        logger = TensorBoardLogger("./tb_logs", name="test")

        # using ddp : https://lightning.ai/pages/community/tutorial/distributed-training-guide/
        callbacks = [
            ModelCheckpoint(
                save_top_k=1, mode="max", monitor="valid_acc"
            ),  # save top 1 model
            LearningRateMonitor(logging_interval='epoch'),
        ]
        trainer = pl.Trainer(
            max_epochs=10,
            callbacks=callbacks,
            accelerator="auto",  # Uses GPUs or TPUs if available
            devices="auto",
            strategy="ddp",
            precision="16-mixed",
            deterministic=True,
            logger=logger,
        )
        p = Process(target=trainer.fit, name="testServeurPL",args=[lightningModel],kwargs=dict(datamodule=dataModule))
        p.start()
        print("PID",p.pid)
        p.join()
        p.close()


    return str(model)
