import torch
import torch.nn as nn
import torch.optim as optim
import mlflow.pytorch
import mlflow.utils.mlflow_tags
from datasets.loader import get_dataloaders, get_input_example
from common.utils.config import load_config
from common.utils.instantiate import get_class_from_string
from common.utils.perf import log_system_metrics, log_gpu_metrics

def evaluate_model(model, test_loader, device):
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

def train_step(model, train_loader, criterion, optimizer, device):
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

def train(cfg):
   device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
   train_loader, test_loader = get_dataloaders(cfg.data.path, cfg.train.batch_size, cfg.train.num_workers)

   model_class = get_class_from_string(cfg.models[cfg.train.model].class_path)
   model = model_class(num_classes=cfg.data.num_classes).to(device)
   criterion = nn.CrossEntropyLoss()
   optimizer = optim.Adam(model.parameters(), lr=cfg.train.lr)

   acc = None
   for epoch in range(1, cfg.train.epochs + 1):
         log_system_metrics(step=epoch)  # just a unique step offset
         log_gpu_metrics(step=epoch)
         loss = train_step(model, train_loader, criterion, optimizer, device)
         acc = evaluate_model(model, test_loader, device)
         mlflow.log_metric("loss", loss, step=epoch)
         mlflow.log_metric("accuracy", acc, step=epoch)
         print(f"Epoch {epoch}: loss={loss:.4f}, accuracy={acc:.4f}")

   input_example = get_input_example()
   signature = model.get_signature(input_example)
   mlflow.pytorch.log_model(model, "model", input_example=input_example.cpu().numpy(), signature=signature)
   return model, acc

def main():
   cfg = load_config()
   train(cfg)

if __name__ == "__main__":
   main()
