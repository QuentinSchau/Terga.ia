import lightning.pytorch as pl
import numpy as np
import torch
from torch.utils.data import DataLoader

from app.model.dataset.DummyClassifyingDataset import DummyClassifyingDataset


class DummyDataModule(pl.LightningDataModule):
    r"""
    DummyDataModule class use for train, validation and test.
    """

    def __init__(self, dataModuleParam: dict):
        r"""
        :param dataModuleParam: dict which contains :
        - "numberFeatures" : int, it's the number of features to use
        - "numberLabels" : int or tuple, it's the number of labels to predict
        OPTIONAL :
        - "dataType" : numpy.dtype, the type of data to use, default is np.float32
        - "numberRows" : the number of rows to use , default is 100
        - "dataloaderArgs" : dict for define dataloader args see here https://pytorch.org/docs/stable/data.html :

        """
        super().__init__()
        self.dataModuleParam = dataModuleParam

    def setup(self, stage=None):

        if not "numberFeatures" in self.dataModuleParam: raise ValueError("numberFeatures is not define in "
                                                                          "dataModuleParam see the doc")
        if not "numberLabels" in self.dataModuleParam: raise ValueError("numberLabels is not define in "
                                                                        "dataModuleParam see the doc")

        # dataset
        self.trainDataset = self.validationDataset = self.testDataset = \
            DummyClassifyingDataset(self.dataModuleParam["dataType"] if "dataType" in self.dataModuleParam else torch.float,
                                    self.dataModuleParam["numberFeatures"],
                                    self.dataModuleParam["numberRows"] if "numberRows" in self.dataModuleParam else 100,
                                    self.dataModuleParam["numberLabels"])

    def train_dataloader(self):
        train_loader = DataLoader(
            dataset=self.trainDataset,
            **self.dataModuleParam["dataloaderArgs"] if "dataloaderArgs" in self.dataModuleParam else None)
        return train_loader

    def val_dataloader(self):
        validation_loader = DataLoader(
            dataset=self.validationDataset,
            **self.dataModuleParam["dataloaderArgs"] if "dataloaderArgs" in self.dataModuleParam else None)
        return validation_loader

    def test_dataloader(self):
        test_loader = DataLoader(
            dataset=self.testDataset,
            **self.dataModuleParam["dataloaderArgs"] if "dataloaderArgs" in self.dataModuleParam else None)
        return test_loader
