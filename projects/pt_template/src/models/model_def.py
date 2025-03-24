import torch.nn as nn
import torch.nn.functional as F

class ProjectModel(nn.Module):
    def __init__(self, num_classes=26):
        super().__init__()
        # Definition goes here

    def forward(self, x):
        # computations
        return self.fc2(x)
