#!/usr/bin/env bash

# Check if script was sourced (works in Bash and Zsh)
if [[ "${FUNCNAME[0]}" == "source" ]] || [ -n "$ZSH_EVAL_CONTEXT" ] && [[ "$ZSH_EVAL_CONTEXT" == *:file ]]; then
   : # sourced, do nothing
else
   echo "[ERROR] You must source this script: use 'source ./local.sh' or '. ./local.sh'"
   return 1 2>/dev/null || exit 1
fi

set -e

# Log function with UTC timestamp
log() {
   echo "[$(date -u +'%Y-%m-%dT%H:%M:%SZ')] $1"
}

# Load .env from docker
ENV_FILE="../docker/.env"
if [ ! -f "$ENV_FILE" ]; then
   echo "[ERROR] .env file not found at $ENV_FILE"
   return 1 2>/dev/null || exit 1
fi

log "Sourcing .env file..."
set -a
source "$ENV_FILE"
set +a

# Validate env vars
if [ -z "$ACTIVE_PROJECT" ] || [ -z "$COMPOSE_PROJECT_NAME" ]; then
   echo "[ERROR] ACTIVE_PROJECT and COMPOSE_PROJECT_NAME must be set in .env"
   return 1 2>/dev/null || exit 1
fi

## mlops root (should get absolute on both mac and linux)
MLOPS_ROOT=$(cd ../ && pwd -P)
PROJECT_ROOT="$MLOPS_ROOT/projects/$ACTIVE_PROJECT"

VENV_ROOT="$PROJECT_ROOT/.venv"
VENV_PATH="$VENV_ROOT/$COMPOSE_PROJECT_NAME"

# Create venv root if needed
if [ ! -d "$VENV_ROOT" ]; then
   log "Creating virtual env directory: $VENV_ROOT"
   mkdir -p "$VENV_ROOT"
fi

# Create virtual env if missing
if [ ! -d "$VENV_PATH" ]; then
   log "Creating virtual environment at $VENV_PATH"
   python3 -m venv "$VENV_PATH" || {
      echo "[ERROR] Failed to create virtual environment"
      return 1 2>/dev/null || exit 1
   }
else
   log "Virtual environment already exists at $VENV_PATH"
fi

# Activate venv
log "Activating virtual environment..."
# shellcheck disable=SC1090
source "$VENV_PATH/bin/activate"

# Install debugpy
log "Installing debugpy..."
pip install debugpy || {
   echo "[ERROR] Failed to install debugpy"
   return 1 2>/dev/null || exit 1
}

# Install requirements
REQ_FILE="$PROJECT_ROOT/requirements.txt"
if [ ! -f "$REQ_FILE" ]; then
   echo "[ERROR] requirements.txt not found at $REQ_FILE"
   return 1 2>/dev/null || exit 1
fi

log "Installing requirements from $REQ_FILE..."
pip install -r "$REQ_FILE" || {
   echo "[ERROR] Failed to install requirements"
   return 1 2>/dev/null || exit 1
}

# Where output folders create by the container? Do we want to take ownership?
EPHEMERAL_PATH="$PROJECT_ROOT/ephemeral"

if [ -d "$EPHEMERAL_PATH" ]; then
   ROOT_OWNED=$(find "$EPHEMERAL_PATH" -maxdepth 1 -exec stat -c "%U" {} 2>/dev/null \; 2>/dev/null | grep -q '^root$' && echo "yes" || echo "no")

   # macOS fallback for stat
   if [ "$ROOT_OWNED" = "no" ] && stat -f "%Su" "$EPHEMERAL_PATH" &>/dev/null; then
      ROOT_OWNED=$(find "$EPHEMERAL_PATH" -maxdepth 1 -exec stat -f "%Su" {} \; | grep -q '^root$' && echo "yes" || echo "no")
   fi

   if [ "$ROOT_OWNED" = "yes" ]; then
      echo "[WARN] Some files in $EPHEMERAL_PATH are owned by root."
      echo -n "Take ownership and fix permissions? [y/N]: "
      read -r RESPONSE
      if [[ "$RESPONSE" =~ ^[Yy]$ ]]; then
         sudo chown -R "$(whoami):$(whoami)" "$EPHEMERAL_PATH"
         echo "[INFO] Ownership of $EPHEMERAL_PATH updated."
      else
         echo "[INFO] Skipped permission fix."
      fi
   fi
fi

# Clean old paths from PYTHONPATH
PYTHONPATH=$(echo "$PYTHONPATH" | tr ':' '\n' | grep -v "$MLOPS_ROOT" | tr '\n' ':' | sed 's/:$//')

# Set PYTHONPATH to project src and common
export PYTHONPATH="$PROJECT_ROOT/src:$MLOPS_ROOT:$PYTHONPATH"
log "PYTHONPATH set to: $PYTHONPATH"

log "Environment ready for development. Run 'deactivate' to exit"