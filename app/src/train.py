import torch
import torch.nn as nn
import torch.optim as optim
import mlflow
import mlflow.pytorch
import yaml
import os
import mlflow.utils.mlflow_tags
from utils.naming import generate_random_suffix

from models.cnn import SimpleCNN
from datasets.emnist_loader import get_emnist_dataloaders


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


def evaluate(model, test_loader, device):
   model.eval()
   correct = 0
   total = 0
   with torch.no_grad():
      for images, labels in test_loader:
         images, labels = images.to(device), labels.to(device)
         outputs = model(images)
         _, predicted = torch.max(outputs, 1)
         correct += (predicted == labels).sum().item()
         total += labels.size(0)
   return correct / total


def main():
   config = load_config()
   device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
   train_loader, test_loader = get_emnist_dataloaders()

   model = SimpleCNN(num_classes=config["model"]["num_classes"]).to(device)
   criterion = nn.CrossEntropyLoss()
   optimizer = optim.Adam(model.parameters(), lr=config["training"]["lr"])

   mlflow.set_experiment(config["experiment"]["name"])
   with mlflow.start_run() as run:
      # Compose custom run name
      custom_prefix = config["experiment"].get("run_prefix", "trial")
      random_suffix = generate_random_suffix()
      run_name = f"{custom_prefix}-{random_suffix}"

      mlflow.set_tag(mlflow.utils.mlflow_tags.MLFLOW_RUN_NAME, run_name)
      mlflow.log_params({
         "num_classes": config["model"]["num_classes"],
         "learning_rate": config["training"]["lr"],
         "epochs": config["training"]["epochs"]
      })

      for epoch in range(1, config["training"]["epochs"] + 1):
         loss = train(model, train_loader, criterion, optimizer, device)
         acc = evaluate(model, test_loader, device)
         mlflow.log_metric("loss", loss, step=epoch)
         mlflow.log_metric("accuracy", acc, step=epoch)
         print(f"Epoch {epoch}: loss={loss:.4f}, accuracy={acc:.4f}")

      mlflow.pytorch.log_model(model, "model")

      mlflow.register_model(
         model_uri=f"runs:/{run.info.run_id}/model",
         name=config["experiment"].get("model_name", "handwritten-cnn")
      )


if __name__ == "__main__":
   main()
