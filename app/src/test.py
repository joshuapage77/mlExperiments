# src/test.py
import torch
import mlflow
from models.cnn import SimpleCNN  # adjust if your model file is named differently
from datasets.loader import get_test_loader  # placeholder for your dataset loader

def evaluate(model, dataloader, device):
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in dataloader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, preds = torch.max(outputs, 1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)
    return correct / total

def main():
    mlflow.set_experiment("handwritten-classifier")
    with mlflow.start_run(run_name="evaluation"):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        model = SimpleCNN()
        model.load_state_dict(torch.load("model.pth"))  # change path as needed
        model.to(device)

        test_loader = get_test_loader(batch_size=64)
        accuracy = evaluate(model, test_loader, device)

        mlflow.log_metric("test_accuracy", accuracy)
        print(f"Test Accuracy: {accuracy:.4f}")

if __name__ == "__main__":
    main()
