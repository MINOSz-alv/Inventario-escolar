#!/usr/bin/env bash
set -euo pipefail

# Export MongoDB database for the app (BSON and per-collection JSON)
# Usage:
#   MONGO_URI='mongodb://user:pass@host:27017' MONGO_DB_NAME=cecytem_db ./scripts/export_mongo.sh /path/to/outdir
# or
#   export MONGO_URI='...'; export MONGO_DB_NAME='cecytem_db'; ./scripts/export_mongo.sh

MONGO_URI="${MONGO_URI:-mongodb://localhost:27017/}"
MONGO_DB="${MONGO_DB_NAME:-cecytem_db}"
OUTDIR="${1:-./mongo_export}"
TIMESTAMP=$(date -u +"%Y%m%dT%H%M%SZ")
OUTPATH="$OUTDIR/${MONGO_DB}-${TIMESTAMP}"

mkdir -p "$OUTPATH"

echo "Mongo export starting"
echo "  URI: $MONGO_URI"
echo "  DB : $MONGO_DB"
echo "  Out: $OUTPATH"

# BSON dump with mongodump if available
if command -v mongodump >/dev/null 2>&1; then
  echo "Running mongodump..."
  mongodump --uri="$MONGO_URI" --db="$MONGO_DB" --out="$OUTPATH/dump"
  echo "mongodump completed: $OUTPATH/dump"
else
  echo "mongodump not found in PATH; skipping BSON dump" >&2
fi

# JSON exports per-collection with mongoexport if available
if command -v mongoexport >/dev/null 2>&1; then
  echo "Running mongoexport for collections: items, categories, locations"
  for coll in items categories locations; do
    echo "  exporting $coll to $OUTPATH/${coll}.json"
    mongoexport --uri="$MONGO_URI" --db="$MONGO_DB" --collection="$coll" --out="$OUTPATH/${coll}.json" --jsonArray || echo "Failed exporting $coll" >&2
  done
  echo "mongoexport completed: $OUTPATH/*.json"
else
  echo "mongoexport not found in PATH; skipping JSON exports" >&2
fi

echo "Export finished: $OUTPATH"

# Helpful reminder
cat <<EOF > "$OUTPATH/README.txt"
This export contains BSON dump (mongodump) and/or per-collection JSON (mongoexport).
To restore BSON dump: mongorestore --uri="${MONGO_URI}" --nsInclude="${MONGO_DB}.*" $OUTPATH/dump/${MONGO_DB}
To import JSON into a collection: mongoimport --uri="${MONGO_URI}" --db="${MONGO_DB}" --collection=items --file="$OUTPATH/items.json" --jsonArray
EOF

echo "Wrote README at $OUTPATH/README.txt"
