import torch
import torch.nn as nn


class CNN(nn.Module):
    def __init__(self) -> None:
        super(CNN, self).__init__()

        self.conv1 = nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3)
        self.relu1 = nn.ReLU()

        self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3)
        self.relu2 = nn.ReLU()

        self.fc1 = nn.Linear(1916*1076*32, 5)

    def forward(self, x):
        x = self.conv1(x)
        x = self.relu1(x)
        x = self.conv2(x)
        x = self.relu2(x)
        x = x.view(x.size(0), -1)
        x = self.fc1(x)
        return x

if __name__ == "__main__":
    model = CNN()
    size = (1,3,1920,1080)
    x = torch.rand(size)
    print(model.forward(x))
