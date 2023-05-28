from enum import Enum
import os

growthStage = {
    "出苗期": 0,
    "三叶期": 1,
    "拔节期": 2,
    "穗期": 3,
    "花粒期": 4
}

datasetVolumnRatio = {
    "train": 0.8,
    "validate": 0.1,
    "test": 0.1
}

def CountFilesInDirectory(dirPath):
    return len(os.listdir(dirPath))