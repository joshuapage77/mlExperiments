import psutil
import mlflow
import subprocess

def log_system_metrics(step=None):
   mlflow.log_metric("cpu_percent", psutil.cpu_percent(), step=step)
   mem = psutil.virtual_memory()
   mlflow.log_metric("memory_used_mb", mem.used / 1024**2, step=step)

def log_gpu_metrics(step=None):
   try:
      output = subprocess.check_output(
         ["nvidia-smi", "--query-gpu=utilization.gpu,memory.used", "--format=csv,noheader,nounits"],
         encoding="utf-8"
      )
      gpu_util, mem_used = map(int, output.strip().split(", "))
      mlflow.log_metric("gpu_util_percent", gpu_util, step=step)
      mlflow.log_metric("gpu_mem_used_mb", mem_used, step=step)
   except Exception:
      pass  # skip if not available