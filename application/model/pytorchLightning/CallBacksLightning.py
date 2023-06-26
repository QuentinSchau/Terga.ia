import lightning


class CallBacksLightning:
    r"""
        Class that implement a list of callBacks to apply to a Trainer of Pytorch Lightning.

        You should define it by pass a dict (json) to instantiate it. Your dict can be composed with a list of callbacks.
        You can add callbacks later by passing a dict or lightning.pytorch.callbacks object.
        If you pass a dict, your the name of callback should be a lightning.pytorch.callbacks class.

        EXEMPLE :
        {
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
        }
        """

    listCallBacks: list

    def __init__(self,callBacksParameters = None):
        self.listCallBacks = []
        if callBacksParameters is not None:
            if not "callbacks" in callBacksParameters : raise ValueError("The callbacks parameters should contain a list of callback")

            for callbackParam in callBacksParameters["callbacks"]:
                if not hasattr(lightning.pytorch.callbacks, callbackParam["callback"]): raise ValueError(
                    "callback attribute of the callBackParameters is not class from lightning.pytorch.callbacks module")
                callback = getattr(lightning.pytorch.callbacks, callbackParam['callback'])(**callbackParam['callbackArgs']) \
                    if 'callbackArgs' in callbackParam else getattr(lightning.pytorch.callbacks, callbackParam['callback'])()
                self.listCallBacks.append(callback)

