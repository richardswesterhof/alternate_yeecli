#!/usr/bin/env bash
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
if [[ -n "$DEBUG" ]]; then
  echo "$SCRIPT_DIR"
fi
source "$SCRIPT_DIR/venv/bin/activate"
python "$SCRIPT_DIR/main.py" "$@"
deactivate