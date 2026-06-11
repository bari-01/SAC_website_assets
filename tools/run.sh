#!/bin/bash
# Run the SAC Asset Pipeline using UV
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
ASSETS_DIR="${1:-$PROJECT_DIR/assets}"

if [ ! -d "$ASSETS_DIR" ]; then
    echo "Assets directory not found: $ASSETS_DIR"
    exit 1
fi

cd "$SCRIPT_DIR"
PYTHONPATH="" uv run python process_assets.py "$ASSETS_DIR" "$@"
