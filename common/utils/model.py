import mlflow
import torch

def get_signature(self, input_example):
   input_example = input_example.to(next(self.parameters()).device)
   with torch.no_grad():
      output = self(input_example)
   return mlflow.models.infer_signature(input_example.cpu().numpy(), output.cpu().numpy())