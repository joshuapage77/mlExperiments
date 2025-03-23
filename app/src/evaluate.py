import torch
import mlflow
import mlflow.pytorch
import yaml
import os
import sys
from mlflow.tracking import MlflowClient

from datasets.emnist_loader import get_emnist_dataloaders


def load_config():
   config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
   with open(config_path, "r") as f:
      return yaml.safe_load(f)


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


def get_model_uri(model_name, override_version=None):
   if override_version:
      return f"models:/{model_name}/{override_version}"
   client = MlflowClient()
   latest_unpromoted = [
      v for v in client.get_latest_versions(model_name, stages=[])
      if v.current_stage == 'None'
   ]
   if not latest_unpromoted:
      raise Exception(f"No unpromoted versions found for model '{model_name}'")
   return f"models:/{model_name}/{latest_unpromoted[-1].version}"


def main():
   config = load_config()
   device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

   _, test_loader = get_emnist_dataloaders()
   model_name = config["experiment"].get("model_name", "handwritten-cnn")
   version_override = sys.argv[1] if len(sys.argv) > 1 else None
   model_uri = get_model_uri(model_name, version_override)

   model = mlflow.pytorch.load_model(model_uri).to(device)
   accuracy = evaluate(model, test_loader, device)

   mlflow.set_experiment(f"{model_name}-evaluation")
   with mlflow.start_run():
      mlflow.log_param("model_uri", model_uri)
      mlflow.log_metric("accuracy", accuracy)
      print(f"✅ Evaluation Accuracy: {accuracy:.4f}")
      client = MlflowClient()
      version = model_uri.split("/")[-1]
      version_info = client.get_model_version(name=model_name, version=str(version))
      source_run_id = version_info.run_id

      source_run = client.get_run(source_run_id)
      source_experiment_id = source_run.info.experiment_id
      source_run_name = source_run.data.tags.get("mlflow.runName", "")

      mlflow.set_tag("source_run_id", source_run_id)
      mlflow.set_tag("source_experiment_id", source_experiment_id)
      mlflow.set_tag("source_run_name", source_run_name)


if __name__ == "__main__":
   main()
