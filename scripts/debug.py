# scripts/debug.py
import debugpy
import sys
import os
import runpy

def fail(msg):
   print(f"[ERROR] {msg}", flush=True)
   sys.exit(1)

if len(sys.argv) < 2:
   fail("Usage: python scripts/debug.py <target_script.py> [args...]")

target_script = sys.argv[1]

if not os.path.exists(target_script):
   fail(f"Target script not found: {target_script}")

if not target_script.endswith(".py"):
   fail(f"Not a Python script: {target_script}")

print(f"[INFO] Launching: {target_script}", flush=True)

try:
   debugpy.listen(("0.0.0.0", 5678))
   print("[INFO] Debugger listening on port 5678...", flush=True)
   debugpy.wait_for_client()
except Exception as e:
   fail(f"Debugpy failed to start or listen: {e}")

# Override sys.argv to pass through script arguments
sys.argv = [target_script] + sys.argv[2:]

try:
   runpy.run_path(target_script, run_name="__main__")
except Exception as e:
   fail(f"Failed to run target script: {e}")
