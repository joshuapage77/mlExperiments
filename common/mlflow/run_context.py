import mlflow
from mlflow.utils.mlflow_tags import MLFLOW_RUN_NAME
from common.mlflow.helper import log_model
from common.utils.naming import assemble_run_name

class MLflowRunContext:
   _counter = -1
   def __init__(self, cfg, model=None, phase="train", run_mode="single", session_name="noname"):
      self.__class__._counter += 1
      self.suffix = self.__class__._counter
      self.cfg = cfg
      self.model = model
      self.phase = phase
      self.run = None
      self.session_name = session_name
      self.run_mode = run_mode
      self.run_name = assemble_run_name(cfg.project.run_prefix, self.run_mode, self.session_name, self.suffix)
      self.metric = None
      self.model_name = None

   def __enter__(self):
      mlflow.set_experiment(self.cfg.project.name)

      self.run = mlflow.start_run(run_name=self.run_name, tags={
         "project": self.cfg.project.name,
         MLFLOW_RUN_NAME: self.run_name,
      })

      # Log standard config if relevant
      if hasattr(self.cfg, "data") and hasattr(self.cfg.data, "num_classes"):
         mlflow.log_param("num_classes", self.cfg.data.num_classes)

      if hasattr(self.cfg, "train") and self.phase == "train":
         for key, value in self.cfg.train.items():
            mlflow.log_param(key, value)

      commit = self.cfg.git.commit
      mlflow.set_tag("git.commit", commit)
   
      self.model_name = f"{self.cfg.models[self.cfg.train.model].name}-{commit[:7]}"
      print(f"Model Name: {self.model_name}")
      mlflow.set_tag("model.name", self.model_name)

      return self.run

   def __exit__(self, exc_type, exc_val, exc_tb):      
      log_model(self.model)
      mlflow.register_model(
         model_uri=f"runs:/{self.run.info.run_id}/model",
         name=self.model_name
      )
      
      mlflow.end_run()

