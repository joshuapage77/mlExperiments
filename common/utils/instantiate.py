import importlib

def get_class_from_string(dotted_path: str):
   module_path, class_name = dotted_path.rsplit(".", 1)
   module = importlib.import_module(module_path)
   return getattr(module, class_name)