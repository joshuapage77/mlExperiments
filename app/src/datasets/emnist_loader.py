import torch
from torchvision.datasets import EMNIST
from torch.utils.data import DataLoader
from torchvision import transforms

class AdjustLabel(torch.nn.Module):
   def forward(self, x):
      return x - 1

def get_emnist_dataloaders(batch_size=64, num_workers=2):
   transform = transforms.Compose([
      transforms.ToTensor(),
      transforms.Normalize((0.1307,), (0.3081,))
   ])

   label_transform = AdjustLabel()

   train_dataset = EMNIST(
      root="data",
      split="letters",
      train=True,
      download=True,
      transform=transform,
      target_transform=label_transform
   )

   test_dataset = EMNIST(
      root="data",
      split="letters",
      train=False,
      download=True,
      transform=transform,
      target_transform=label_transform
   )

   train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers)
   test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers)

   return train_loader, test_loader