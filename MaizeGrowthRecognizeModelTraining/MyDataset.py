import csv
from enum import Enum
from PIL import Image
import torch
from torch.utils.data import Dataset
from torchvision.transforms import transforms

class DatasetType(Enum):
    Train:0
    Validate:1
    Test:2


class MyDataset(Dataset):
    def __init__(self,datasetType) -> None:
        if datasetType == DatasetType.Train:
            datasetPath = "./data/train"
        if datasetType == DatasetType.Validate:
            datasetPath = "./data/validate"
        if datasetType == DatasetType.Test:
            datasetPath = "./data/test"

        targetFile = open(datasetPath+"/target.csv","r")
        targetReader = csv.reader(targetFile)

        self.data = []
        self.target = []
        for line in targetReader:
            image = transforms.ToTensor(Image.open(datasetPath+"/"+line[0]))
            self.data.append(image)
            self.target.append(line[1])

    def __len__(self):
        return len(self.target)

    def __getitem__(self, index):
        x = self.data[index]
        y = self.target[index]
        return (x, y)
        
