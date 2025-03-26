import torch
import mlflow
import mlflow.data
import numpy as np
from torchvision.datasets import EMNIST
from torch.utils.data import DataLoader
from torchvision import transforms

class AdjustLabel(torch.nn.Module):
   def forward(self, x):
      return x - 1

def get_dataloaders(data_path="data", batch_size=64, num_workers=2):
   transform = transforms.Compose([
      transforms.ToTensor(),
      transforms.Normalize((0.1307,), (0.3081,))
   ])

   label_transform = AdjustLabel()

   train_dataset = EMNIST(
      root=data_path,
      split="letters",
      train=True,
      download=True,
      transform=transform,
      target_transform=label_transform
   )

   test_dataset = EMNIST(
      root=data_path,
      split="letters",
      train=False,
      download=True,
      transform=transform,
      target_transform=label_transform
   )

   X_np = train_dataset.data.numpy().reshape(-1, 28 * 28)
   dataset = mlflow.data.from_numpy(X_np, source="torchvision.EMNIST", name="EMNIST")
   mlflow.log_input(dataset, context="training")

   train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers)
   test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers)

   return train_loader, test_loader

def get_input_example():
   # Create a dummy input matching the expected shape
   channels = 1
   height = 28
   width = 28
   input_tensor = torch.rand(1, channels, height, width).to(torch.float32)
   return input_tensor