import mlflow
import torch

def main():
    with mlflow.start_run():
        mlflow.log_param("example_param", 123)
        print("Training loop would go here...")

if __name__ == "__main__":
    main()
