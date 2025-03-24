import mlflow
from mlflow.tracking import MlflowClient
from mlflow.utils.mlflow_tags import MLFLOW_RUN_NAME
from common.utils.naming import generate_random_suffix

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


def log_evaluation_results(model_name: str, model_uri: str, accuracy: float):
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

def run_training_and_log(config, model, train_loader, test_loader, criterion, optimizer, device, train_fn, evaluate_fn):
   mlflow.set_experiment(config["project"]["name"])

   with mlflow.start_run() as run:
      custom_prefix = config["project"].get("run_prefix", "trial")
      run_name = f"{custom_prefix}-{generate_random_suffix()}"
      mlflow.set_tag(MLFLOW_RUN_NAME, run_name)

      mlflow.log_params({
         "num_classes": config["model"]["num_classes"],
         "learning_rate": config["training"]["lr"],
         "epochs": config["training"]["epochs"]
      })

      for epoch in range(1, config["training"]["epochs"] + 1):
         loss = train_fn(model, train_loader, criterion, optimizer, device)
         acc = evaluate_fn(model, test_loader, device)
         mlflow.log_metric("loss", loss, step=epoch)
         mlflow.log_metric("accuracy", acc, step=epoch)
         print(f"Epoch {epoch}: loss={loss:.4f}, accuracy={acc:.4f}")

      mlflow.register_model(
         model_uri=f"runs:/{run.info.run_id}/model",
         name=config["project"].get("model_name", "unnamed_model")
      )