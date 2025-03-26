import random
from pathlib import Path

_animal_list = None

def generate_padded_number(min_val: int, max_val: int, length: int) -> str:
   num = random.randint(min_val, max_val)
   return str(num).zfill(length)

def random_animal() -> str:
   global _animal_list
   if _animal_list is None:
      animal_file = Path(__file__).parent.parent / "assets" / "animals.txt"
      with animal_file.open("r") as f:
         _animal_list = [line.strip() for line in f if line.strip()]
   return random.choice(_animal_list)

def assemble_run_name(run_prefix, run_mode, session_name, suffix):
   actual_suffix = f"-{suffix}" if run_mode=="multi" else ""
   return f"{run_prefix}-{run_mode}-{session_name}{actual_suffix}"