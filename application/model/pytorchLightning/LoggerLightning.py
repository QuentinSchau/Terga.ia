import lightning


class LoggerLightning:
    r"""
        Class that implement a logger to apply to a Trainer of Pytorch Lightning.

        You should define it by pass a dict (json) to instantiate it. The dict has to contain the name of logger that must be a
         lightning.pytorch.loggers class.

        EXEMPLE :
        {
            "logger": {
                "loggerName": "TensorBoardLogger",
                "loggerArgs": {
                    "save_dir": "./tb_logs",
                    "name": "test"
                }
            }
        }
        """

    def __init__(self,loggerParameters):
        if not "logger" in loggerParameters : raise ValueError("The logger parameters should contain a logger")

        if not hasattr(lightning.pytorch.loggers, loggerParameters["logger"]["loggerName"]): raise ValueError(
            "logger attribute of the loggerParameters is not class from lightning.pytorch.loggers module")
        self.logger = getattr(lightning.pytorch.loggers, loggerParameters['logger']["loggerName"])(**loggerParameters['logger']["loggerArgs"]) \
            if 'loggerArgs' in loggerParameters["logger"] else getattr(lightning.pytorch.loggers, loggerParameters['logger']['loggerName'])()


