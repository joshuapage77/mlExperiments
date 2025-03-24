import torch
import mlflow
import mlflow.pytorch
import sys
from mlflow.tracking import MlflowClient
from common.utils.config import load_config
from common.mlflow.helper import get_model_uri
from common.mlflow.helper import log_evaluation_results, get_dataloaders

def evaluate(model, test_loader, device):
   model.eval()
   correct = 0
   total = 0
   # with torch.no_grad():
      # Implement Logic
   return correct / total


def main():
   config = load_config()
   device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

   _, test_loader = get_dataloaders()
   model_name = config["project"].get("model_name", "unnamed_model")
   version_override = sys.argv[1] if len(sys.argv) > 1 else None
   model_uri = get_model_uri(model_name, version_override)

   model = mlflow.pytorch.load_model(model_uri).to(device)
   accuracy = evaluate(model, test_loader, device)

   log_evaluation_results(model_name, model_uri, accuracy)

if __name__ == "__main__":
   main()
