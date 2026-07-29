#!/usr/bin/env bash
set -euo pipefail

# Wrapper to initialize local MongoDB for the project
# Usage examples:
#   ./scripts/init_mongo.sh
#   MONGO_URI='mongodb://localhost:27017/' MONGO_DB_NAME=cecytem_db ./scripts/init_mongo.sh
#   CREATE_MONGO_USER=true MONGO_INIT_USER=appuser MONGO_INIT_PWD=pass ./scripts/init_mongo.sh

PYTHON="${PYTHON:-python3}"
SCRIPT="$(dirname "$0")/init_mongo.py"

if [ ! -f "$SCRIPT" ]; then
  echo "Script not found: $SCRIPT" >&2
  exit 2
fi

echo "Running init script with PYTHON=$PYTHON"
$PYTHON "$SCRIPT"

# After init, offer an export
if command -v mongodump >/dev/null 2>&1; then
  echo "Creating a quick mongodump export..."
  ./scripts/export_mongo.sh
fi

echo "Done."
