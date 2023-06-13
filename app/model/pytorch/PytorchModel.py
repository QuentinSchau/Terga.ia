import torch.nn as nn
from functools import reduce
from app.model.pytorch.Layer import Layer


class PytorchModel(nn.Module):
    r"""
        PytorchModel Class implement a Pytorch Model.

        PARAMETER : This model is instantiate with dict object.
        This dict has to contain :
        - "architecture" : Architecture which is a list of Layer
        - "lossFunction" : Loss Function from torch.nn
        - "lossFunctionArgs" : Loss function args

        EXEMPLE :

        {
            "architecture": [
                {
                    "layer": "Linear",
                    "layerArgs": {
                        "in_features": 65,
                        "out_features": 8
                    },
                    "activationFunction": "Relu"
                },
                {
                    "layer": "Linear",
                    "layerArgs": {
                        "in_features": 8,
                        "out_features": 8
                    },
                    "activationFunction": "Relu"
                }
            ],
            "lossFunction": "CrossEntropyLoss",
            "lossFunctionArgs": {
                "reduction": "mean"
            }
        }
    """
    def __init__(self, modelParams):
        super(PytorchModel, self).__init__()

        # Parameters
        self.modelParams = modelParams

        # architecture
        self.layers = nn.ModuleList()

        if not "architecture" in self.modelParams: raise AttributeError("Architecture is missing for create the PytorchModel, see the docs")
        if not "lossFunction" in self.modelParams: raise AttributeError("Loss function is missing for create the PytorchModel, see the docs")
        self.architecture = self.modelParams["architecture"]
        for layer in self.architecture:
            self.layers.append(Layer(layer))

        self.lossFunction = getattr(nn, self.modelParams['lossFunction'])(
            **self.modelParams['lossFunctionArgs']) \
            if 'lossFunctionArgs' in self.modelParams else getattr(nn, self.modelParams['lossFunction'])()

    def forward(self, x):
        return reduce(lambda x, f: f(x), self.layers,x)

    def loss(self, logits, label):
        return self.lossFunction(logits,label)
