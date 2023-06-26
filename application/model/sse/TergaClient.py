
from application.model.pytorch.PytorchModel import PytorchModel
from application.model.pytorchLightning.CallBacksLightning import CallBacksLightning
from application.model.pytorchLightning.Datamodule import DummyDataModule
from application.model.pytorchLightning.LightningModel import LightningModel
from application.model.pytorchLightning.LoggerLightning import LoggerLightning
from application.model.pytorchLightning.TrainerLightning import TrainerLightning
from application.model.sse.clientSSE import SSEClient
import json

class TergaClient:
    r"""
    This class implement Terga.ia client. It use on Terga.ia SLAVE Mode.
    """

    def __init__(self, name=None,masterAddress=None,**kwargs):
        super(TergaClient,self).__init__()
        self.name = name
        self.masterAddress = masterAddress
        self.trainer = None
        self.logger = None
        self.callbacks = None

    def subscrib(self):
        self.SSEClient = SSEClient('{0}listen?name={1}'.format(self.masterAddress, self.name))


    def run(self):
        for message in self.SSEClient:
            if message.event == "setTrainer":
                self.setTrainer(json.loads(message.data))
            if message.event == "runTrain":
                self.runTrain(json.loads(message.data))
    def setTrainer(self,trainerParameters):
        self.trainer = TrainerLightning(trainerParameters)

    def setLogger(self,loggerParameters):
        self.logger = LoggerLightning(loggerParameters)

    def setCallbacks(self,callbacksParameters):
        self.callbacks = CallBacksLightning(callbacksParameters)

    def runTrain(self,parameters : dict):
        """
        Method which run a train with pytorch Lightning
        :param parameters: The parameters of train
        :return:
        """
        if not hasattr(parameters,"model") :
            model = PytorchModel(parameters["model"])
        else:
            raise ValueError("model is not defined in the JSON parameters, you should defined it, see the doc")

        dataModule = DummyDataModule(parameters["dataModuleArgs"])
        lightningModel = LightningModel(model, parameters)

        # using ddp : https://lightning.ai/pages/community/tutorial/distributed-training-guide/
        self.trainer.trainer.fit(lightningModel,datamodule=dataModule)