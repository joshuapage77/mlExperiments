import torch.nn as nn
import torch.nn.functional as F
import torch
import mlflow.models

class BaselineModel(nn.Module):
    def __init__(self, num_classes=26):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)   # 28x28 → 28x28
        self.pool1 = nn.MaxPool2d(2, 2)                            # 28x28 → 14x14

        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)  # 14x14 → 14x14
        self.pool2 = nn.MaxPool2d(2, 2)                            # 14x14 → 7x7

        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x):
        x = self.pool1(F.relu(self.conv1(x)))
        x = self.pool2(F.relu(self.conv2(x)))
        x = x.view(x.size(0), -1)  # flatten
        x = F.relu(self.fc1(x))
        return self.fc2(x)

