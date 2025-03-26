import mlflow
from mlflow.tracking import MlflowClient
from urllib.parse import urlparse
import json

def tag_logged_model(model, artifact_path: str, model_uri: str):
   try:
      import torch.nn as nn
      if isinstance(model, nn.Module):
         flavors = ["pytorch"]
      else:
         raise TypeError
   except ImportError:
      flavors = []

   if not flavors:
      try:
         import tensorflow as tf
         if isinstance(model, (tf.Module, tf.keras.Model)):
            flavors = ["tensorflow"]
      except ImportError:
         pass

   if not flavors:
      raise TypeError(f"Unsupported or unknown model type: {type(model)}")

   history = [{
      "run_id": mlflow.active_run().info.run_id,
      "artifact_path": artifact_path,
      "flavors": flavors,
      "model_uri": model_uri
   }]

   mlflow.set_tag("mlflow.log-model.history", json.dumps(history))

def get_model_registry_info(model_name, artifact_path="model"):
   client = MlflowClient()
   model_uri = mlflow.get_artifact_uri(artifact_path)

   # Extract run ID from the artifact URI
   path = urlparse(model_uri).path
   parts = path.strip("/").split("/")
   run_id = parts[2] if len(parts) >= 4 else None
   if run_id is None:
      raise ValueError(f"Could not extract run ID from URI: {model_uri}")

   # Find registered version associated with the run ID
   versions = client.search_model_versions(f"name='{model_name}'")
   version = next((v.version for v in versions if v.run_id == run_id), None)
   if version is None:
      raise ValueError(f"No registered model version found for run ID: {run_id}")

   return {
      "version": version,
      "model_uri": f"models:/{model_name}/{version}",
      "run_id": run_id
   }


# import only if needed, since container won't have all dependencies
def log_model(model, artifact_path="model"):
   try:
      import torch.nn as nn
      if isinstance(model, nn.Module):
         import mlflow.pytorch
         mlflow.pytorch.log_model(model, artifact_path)
         return
   except ImportError:
      pass

   try:
      import tensorflow as tf
      if isinstance(model, (tf.Module, tf.keras.Model)):
         import mlflow.tensorflow
         mlflow.tensorflow.log_model(model, artifact_path)
         return
   except ImportError:
      pass

   raise TypeError(f"Unsupported or unrecognized model type: {type(model)}")

# this could cause an issue if multiple models were training in parallel
def get_model_uri(model_name, override_version=None):
   if override_version:
      return f"models:/{model_name}/{override_version}"

   client = MlflowClient()
   versions = client.search_model_versions(f"name='{model_name}'")
   if not versions:
      raise Exception(f"No versions found for model '{model_name}'")

   latest = sorted(versions, key=lambda v: int(v.version))[-1]
   return f"models:/{model_name}/{latest.version}"