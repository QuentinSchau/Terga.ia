import torch.nn as nn

class Layer(nn.Module):
    r"""
    Layer Class implement one layer of an architecture.

    PARAMETER : This layer is instantiate with dict object.
    This dict has to contain :
    - Pytorch Layer name from torch.nn
    - Layers args
    - Activation function from torch.nn
    - Activation function args

    EXEMPLE :
    {
        "layer": "Linear",
        "layerArgs":
            {
                "in_features":65,
                "out_features":8
            },
        "activationFunction": "ELU",
        "activationFunctionArgs":
            {
                "alpha":0.5
            }
    }
    """
    def __init__(self, layerParam: dict):
        super(Layer, self).__init__()

        self.layerParam = layerParam
        if not hasattr(nn,layerParam["layer"]) : raise ValueError("Layer of the parameters is not class from torch.nn module")
        self.layer = getattr(nn, self.layerParam['layer'])(**self.layerParam['layerArgs']) \
            if 'layerArgs' in self.layerParam else getattr(nn, self.layerParam['layer'])()

        if not hasattr(nn, self.layerParam["activationFunction"]): raise ValueError("Activation Function of the parameters is not class from torch.nn module")
        self.activationFunction = getattr(nn, self.layerParam['activationFunction'])(**self.layerParam['activationFunctionArgs'])\
            if 'activationFunctionArgs' in self.layerParam else getattr(nn, self.layerParam['activationFunction'])()

    def forward(self,x):
        return self.layer(self.activationFunction(x))



