from application.model.databaseModel.Trainning import Trainning
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
    This class implement Terga.ia client. The client will start when you run the Flask app,
    what ever your mode (Slave or Master).

    This class, run train and set all options that users will use with Pytorch Lightning
    """

    def __init__(self, name=None,masterAddress=None,**kwargs):
        super(TergaClient,self).__init__()
        self.name = name
        self.masterAddress = masterAddress
        self.trainerLightning = None
        self.loggerLightning = None
        self.callbacks = None

    def subscrib(self):
        self.SSEClient = SSEClient('{0}listen?name={1}'.format(self.masterAddress, self.name))
        self.run()

    def run(self):
        for message in self.SSEClient:
            try:
                messageData = json.loads(message.data)
                user_id = messageData["user_id"] if "user_id" in messageData else None
                data = messageData["data"] if "data" in messageData else None
                if message.event == "setTrainer":
                    self.setTrainer(data)
                elif message.event == "runTrain":
                    self.runTrain(user_id,data)
                #TODO secure this method with event to ensure that if the event isn't know then throw error
                else : print(message.data)
            except Exception as e:
                print(e)

    def setTrainer(self,trainerParameters):
        self.trainerLightning = TrainerLightning(trainerParameters)
        # if we have not logger in param and if we have logger already defined, add it to the trainer
        if not "logger" in trainerParameters['trainer']["trainerArgs"] and self.loggerLightning is not None : self.trainerLightning.trainer.loggers= [self.loggerLightning.logger]
        # same for callbacks
        if not "callbacks" in trainerParameters['trainer']["trainerArgs"] and self.callbacks is not None : self.trainerLightning.trainer.callbacks.extend(self.callbacks.listCallBacks)

    def setLogger(self,loggerParameters):
        self.loggerLightning = LoggerLightning(loggerParameters)
        if self.trainerLightning is not None: self.trainerLightning.trainer.loggers= [self.loggerLightning.logger]

    def setCallbacks(self,callbacksParameters):
        self.callbacks = CallBacksLightning(callbacksParameters)
        if self.trainerLightning is not None: self.trainerLightning.trainer.callbacks.extend(self.callbacks.listCallBacks)

    def runTrain(self,user_id: int,parameters : dict):
        """
        Method which run a train with pytorch Lightning
        :param user_id: l'identifiant de l'utilisateur qui lance le calcul
        :param parameters: The parameters of train
        :return:
        """
        try:
            if "model" in parameters:
                model = PytorchModel(parameters["model"])
            else:
                raise ValueError("model is not defined in the JSON parameters, you should defined it, see the doc")
            #TODO check if they are Datamodule
            dataModule = DummyDataModule(parameters["dataModuleArgs"])
            lightningModel = LightningModel(model, parameters)
            version = self.trainerLightning.trainer.logger.version
            new_training = Trainning(version=version,name=self.name,user_id=user_id)
            new_training.createTrainning()
            # using ddp : https://lightning.ai/pages/community/tutorial/distributed-training-guide/
            self.trainerLightning.trainer.fit(lightningModel,datamodule=dataModule)
            new_training.isOver()
            new_training.commit()
        except Exception as e:
            print(e)