import torch
from torch.utils.data import IterableDataset, Dataset



class DummyClassifyingDataset(Dataset):
    r"""
    This class implement dummy dataset to test an architecture (for classifying tasks).
    It returns a torch Tensor containing random features. You can choose the number of labels to predict.
    """

    def __init__(self, dataType : torch.dtype, nbFeatures: int,nbRows: int, nbLabels: int):
        r"""
        Create a dummy dataset for classifying tasks.
        :param dataType: The type of data, it must be a torch data type see : https://pytorch.org/docs/stable/tensor_attributes.html#torch.dtype
        :param nbFeatures: it must be the number of features to use
        :param nbRows: it must be the number of rows to use
        :param nbLabels: int or tuple of ints. It must be the number of labels to predict. If the given shape is, e.g.,
        (m, n, k), then  m * n samples are drawn, where values are integer and between 0 and k.
        Default is nbRows, in which case an array of 0 and 1 with nbRows values will be use.
        """
        super(DummyClassifyingDataset, self).__init__()

        # check type of parameters :
        if type(nbRows) != int : raise ValueError("nbRows must be a integer for DummyClassifyingDataset")
        if type(nbFeatures) != int : raise ValueError("nbFeatures must be a integer for DummyClassifyingDataset")
        if type(nbLabels) != int and type(nbLabels) != tuple : raise ValueError("nbLabels must be a integer or tuple for DummyClassifyingDataset")
        self.nbRows = nbRows
        self.data = torch.rand((nbRows,nbFeatures), dtype=dataType)
        self.labels = torch.randint(0,nbLabels,(nbRows,),dtype=torch.long) if type(nbLabels) == int else torch.randint(0,nbLabels[-1],nbLabels[:-1],dtype=torch.long)


    def __getitem__(self, idx):
        return self.data[idx,:], self.labels[idx]

    def __len__(self):
        return self.nbRows


# from collections import deque
#
#
# # Look https://github.com/Lightning-AI/lightning/issues/15734 for explain
# class BranchAndMemorizeIterableDataset(IterableDataset):
#     def __init__(self, path, start=None, end=None, isTrain=False, bufferSize=10000):
#         super(BranchAndMemorizeIterableDataset, self).__init__()
#
#         # read zarr array
#         store = zarr.DirectoryStore(path)
#         self.array = zarr.open(store, mode='r')
#         self.nbRows = self.array.shape[0]
#
#         # define start and end for read array
#         if start is None:
#             start = 0
#         if end is None:
#             end = self.nbRows
#         assert end > start
#         self.start = start
#         self.end = end
#
#         # define batch if we train and want shuffle
#         self.isTrain = isTrain
#         self.bufferSize = bufferSize
#         self.queue = deque([], maxlen=self.bufferSize)
#
#     def __iter__(self):
#         worker_info = torch.utils.data.get_worker_info()
#         if worker_info is None:
#             self.itera = islice(self.array, self.start, self.end)
#         else:
#             world_size = get_world_size()
#             process_rank = get_rank()
#             worker_id = worker_info.id
#             if process_rank == 0:
#                 iter_start = worker_id
#             else:
#                 iter_start = worker_id + (worker_info.num_workers * process_rank)
#             self.itera = islice(self.array, iter_start, None, worker_info.num_workers * world_size)
#         return self
