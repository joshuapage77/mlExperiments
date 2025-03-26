import hydra
from hydra.types import RunMode
from common.mlflow.run_context import MLflowRunContext
from omegaconf import DictConfig
from train import train
from hydra.core.hydra_config import HydraConfig
from common.utils.naming import random_animal
from common.utils.debug import dump_var
import os

config_path=f"{os.getcwd()}/config"
session_name = random_animal()

@hydra.main(config_path=config_path, config_name="config", version_base="1.3")
def run(cfg: DictConfig):
   run_mode = "multi" if HydraConfig.get().mode == RunMode.MULTIRUN else "single"
   print(f"RUN MODE: {run_mode}")
   context = MLflowRunContext(cfg, run_mode=run_mode, session_name=session_name)
   with context:
      context.model, context.metric = train(cfg)
   return context.metric

if __name__ == "__main__":
   run()