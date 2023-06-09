import lightning.pytorch as pl
import torch
import torch.nn as nn
import torchvision
import torchmetrics
import numpy as np
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
import io


# LightningModule that receives a PyTorch model as input
# code inspired from https://github.com/rasbt/deeplearning-models/blob/master/pytorch-lightning_ipynb/mlp/mlp-dropout.ipynb
class LightningModel(pl.LightningModule):
    r"""
           LightningModel Class implement a Pytorch Lightning Module.

           PARAMETER : This model is instantiate with dict object.
           This dict has to contain :
           - "model" : Model which contains architecture and loss function
           - The optimizer to use for train the model :
           "optimizer" :
                {
                    "algorithm" : torch.optim algorithms,
                    "algorithmArgs" :
                        {
                            args for the algorithm choose from torch.optim
                        }
                }
           - "scheduler" : The scheduler to use for adjust the learning rate from torch.optim.lr_scheduler
           - "schedulerArgs" : The scheduler args

           EXEMPLE :
           {
                "model": {
                    "architecture": [
                        {
                            "layer": "Linear",
                            "layerArgs": {
                                "in_features": 10,
                                "out_features": 5
                            },
                            "activationFunction": "Relu"
                        }
                    ],
                    "lossFunction": "CrossEntropyLoss",
                    "lossFunctionArgs": {
                        "reduction": "mean"
                    }
                },
                "optimizer": {
                    "algorithm": "SGD",
                    "algorithmArgs": {
                        "lr": 1e-4
                    }
                },
                "scheduler": "ConstantLR",
                "schedulerArgs": {
                    "factor": 0.5,
                    "total_iters": 10
                }
           }
       """
    def __init__(self, model, modelParams):
        super().__init__()
        self.modelParams=modelParams


        # The inherited PyTorch module
        self.model = model

        # Save settings and hyperparameters to the log directory
        # but skip the model parameters
        self.save_hyperparameters(ignore=["model"])

        # Set up attributes for computing the accuracy
        numClass = self.modelParams["model"]["architecture"][-1]["layerArgs"]["out_features"]
        if numClass > 2 : task = "multiclass"
        else : task = "binary"
        self.train_acc = torchmetrics.Accuracy(task=task, num_classes=numClass)
        self.valid_acc = torchmetrics.Accuracy(task=task, num_classes=numClass)
        self.test_acc = torchmetrics.Accuracy(task=task, num_classes=numClass)
        self.validConfMat = torchmetrics.ConfusionMatrix(task=task, num_classes=numClass)
        self.testConfMat = torchmetrics.ConfusionMatrix(task=task, num_classes=numClass)

    # Defining the forward method is only necessary
    # if you want to use a Trainer's .predict() method (optional)
    def forward(self, x):
        return self.model(x)

    # A common forward step to compute the loss and labels for Map-style dataset
    # this is used for training, validation, and testing below
    def _shared_step(self, batch):
        features, true_labels = batch
        logits = self(features)
        loss = self.model.loss(logits, true_labels)
        predicted_labels = torch.argmax(logits, dim=1)

        return loss, true_labels, predicted_labels


    def training_step(self, batch, batch_idx):

        loss, true_labels, predicted_labels = self._shared_step(batch)
        self.log("train_loss",loss,on_epoch=True,on_step=False,prog_bar=True,sync_dist=True)

        # Do another forward pass in .eval() mode to compute accuracy
        # while accounting for Dropout, BatchNorm etc. behavior
        # during evaluation (inference)
        self.model.eval()
        with torch.no_grad():
            _, true_labels, predicted_labels = self._shared_step(batch)
        self.train_acc.update(predicted_labels, true_labels)
        self.log("train_acc",self.train_acc,on_epoch=True,on_step=False,prog_bar=True,sync_dist=True)
        self.model.train()

        return loss  # this is passed to the optimzer for training


    def validation_step(self, batch, batch_idx):
        loss, true_labels, predicted_labels = self._shared_step(batch)
        self.log("valid_loss",loss,on_epoch=True,on_step=False,prog_bar=True,sync_dist=True)
        self.valid_acc.update(predicted_labels, true_labels)
        self.log("valid_acc",self.valid_acc,on_epoch=True,on_step=False,prog_bar=True,sync_dist=True)
        self.validConfMat.update(predicted_labels, true_labels)


    def test_step(self, batch, batch_idx):
        loss, true_labels, predicted_labels = self._shared_step(batch)
        self.test_acc.update(predicted_labels, true_labels)
        self.testConfMat.update(predicted_labels, true_labels)

    # methode which compute and log the confusion matrix
    def computeAndLogCM(self,confMat,name):
        confMatNorm = confMat.astype('float') / confMat.sum(axis=1)[:, np.newaxis]
        fig,ax = plt.subplots(figsize=(10, 10))
        sns.heatmap(confMatNorm, annot=True, fmt=".2f",ax=ax)
        ax.set_title('Confusion matrix')
        ax.set(xlabel='Predicted label', ylabel='Real label')

        #save image based on https://stackoverflow.com/questions/65498782/how-to-dump-confusion-matrix-using-tensorboard-logger-in-pytorch-lightning
        io_buf = io.BytesIO()
        plt.savefig(io_buf, format='jpeg', bbox_inches='tight')
        io_buf.seek(0)
        im = Image.open(io_buf)
        im = torchvision.transforms.ToTensor()(im)
        self.logger.experiment.add_image(name, im, global_step=self.current_epoch)
        io_buf.close()
        plt.close(fig)

    def on_validation_epoch_end(self):
        confMat = self.validConfMat.compute().cpu().numpy()
        self.computeAndLogCM(confMat,"Confusion matrix on validation")

    def on_test_epoch_end(self):
        self.log("test_acc",self.test_acc,on_epoch=True,on_step=False,prog_bar=True,sync_dist=True)
        confMat = self.testConfMat.compute().cpu().numpy()
        self.computeAndLogCM(confMat,"Confusion matrix on test")

    #########################
    #       OPTIMIZER       #
    #########################

    def configure_optimizers(self):
        # check if the optimizer exist in pytorch optim
        if not hasattr(nn, self.modelParams["optimizer"]): raise ValueError("Optimizer of the parameters is not class "
                                                                           "from torch.nn module")
        optimizer = getattr(torch.optim, self.modelParams['optimizer']['algorithm'])(self.parameters(), **self.modelParams['optimizer']['algorithmArgs']) \
            if 'algorithmArgs' in self.modelParams['optimizer'] \
            else getattr(torch.optim, self.modelParams['optimizer']['algorithm'])(self.parameters())

        # check if we have the scheduler in parameters
        if 'scheduler' in self.modelParams :
            # check if the scheduler exist in pytorch optim
            if not hasattr(torch.optim.lr_scheduler, self.modelParams['scheduler']) : raise ValueError("Scheduler of the parameters is not class"
                                                                                                       "from torch.optim.lr_scheduler")
            lr_scheduler = dict(scheduler=getattr(torch.optim.lr_scheduler, self.modelParams['scheduler'])\
                (optimizer, **self.modelParams['schedulerArgs']) if 'schedulerArgs' in self.modelParams else \
                getattr(torch.optim.lr_scheduler, self.modelParams['scheduler'])(optimizer), name='Learning rate')
        return [optimizer], [lr_scheduler]
