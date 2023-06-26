import lightning

from application.model.pytorchLightning.CallBacksLightning import CallBacksLightning
from application.model.pytorchLightning.LoggerLightning import LoggerLightning


class TrainerLightning:
    r"""
        TrainerLightning Class implement a Trainer of Lightning Module.

        PARAMETER : This trainer is instantiated with dict object.
        This dict has to contain all trainer options
        which can be found here : https://lightning.ai/docs/pytorch/stable/common/trainer.html:

        EXEMPLE :
        {
            "trainer": {
                "trainerName": "Trainer",
                "trainerArgs": {
                    "max_epochs": 10,
                    "callbacks": {
                        "callbacks": [
                            {
                                "callback": "ModelCheckpoint",
                                "callbackArgs": {
                                    "save_top_k": 1,
                                    "mode": "max",
                                    "monitor": "valid_acc"
                                }
                            },
                            {
                                "callback": "LearningRateMonitor",
                                "callbackArgs": {
                                    "logging_interval": "epoch"
                                }
                            }
                        ]
                    },
                    "logger": {
                        "logger": {
                            "loggerName": "TensorBoardLogger",
                            "loggerArgs": {
                                "save_dir": "./tb_logs",
                                "name": "test"
                            }
                        }
                    },
                    "accelerator": "auto",
                    "devices": "auto",
                    "strategy": "ddp",
                    "precision": "16-mixed",
                    "deterministic": true
                }
            }
        }
    """

    def __init__(self,trainerParameters):
        if not "trainer" in trainerParameters : raise ValueError("The trainer parameters should contain a trainer")

        if not hasattr(lightning.pytorch.trainer, trainerParameters["trainer"]["trainerName"]): raise ValueError(
            "trainer attribute of the trainerParameters is not class from lightning.pytorch.trainer module")
        if "callbacks" in trainerParameters['trainer']["trainerArgs"]:
            callbacksModel = CallBacksLightning(trainerParameters['trainer']["trainerArgs"]["callbacks"])
            trainerParameters['trainer']["trainerArgs"]["callbacks"] = callbacksModel.listCallBacks
        if "logger" in trainerParameters['trainer']["trainerArgs"]:
            loggerModel = LoggerLightning(trainerParameters['trainer']["trainerArgs"]["logger"])
            trainerParameters['trainer']["trainerArgs"]["logger"] = loggerModel.logger
        self.trainer = getattr(lightning.pytorch.trainer.trainer, trainerParameters['trainer']["trainerName"])(**trainerParameters['trainer']["trainerArgs"]) \
            if 'trainerArgs' in trainerParameters['trainer'] else getattr(lightning.pytorch.trainer.trainer, trainerParameters['trainer']['trainerName'])()
