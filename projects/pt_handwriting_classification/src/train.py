import os
import yaml
import torch
import torch.nn as nn
import torch.optim as optim
import mlflow.pytorch
import mlflow.utils.mlflow_tags
from common.utils.config import load_config
from models.model_def import ProjectModel
from datasets.loader import get_dataloaders
from evaluate import evaluate
from common.mlflow.helper import run_training_and_log


def load_config():
   config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
   with open(config_path, "r") as f:
      return yaml.safe_load(f)


def train(model, train_loader, criterion, optimizer, device):
   model.train()
   running_loss = 0.0
   for images, labels in train_loader:
      images, labels = images.to(device), labels.to(device)
      outputs = model(images)
      loss = criterion(outputs, labels)
      optimizer.zero_grad()
      loss.backward()
      optimizer.step()
      running_loss += loss.item()
   return running_loss / len(train_loader)

def main():
   config = load_config()
   device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
   train_loader, test_loader = get_dataloaders()

   model = ProjectModel(num_classes=config["model"]["num_classes"]).to(device)
   criterion = nn.CrossEntropyLoss()
   optimizer = optim.Adam(model.parameters(), lr=config["training"]["lr"])

   run_training_and_log(config, model, train_loader, test_loader, criterion, optimizer, device, train, evaluate)

   mlflow.pytorch.log_model(model, "model")


if __name__ == "__main__":
   main()
