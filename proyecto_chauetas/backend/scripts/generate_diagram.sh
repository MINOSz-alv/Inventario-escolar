#!/usr/bin/env bash
set -euo pipefail

# Script para generar diagram.pdf desde diagram.mmd
# Preferirá Docker (minlag/mermaid-cli), si no está disponible intentará npx mmdc.

INPUT="diagram.mmd"
OUTPDF="diagram.pdf"

if [ ! -f "$INPUT" ]; then
  echo "Archivo $INPUT no encontrado." >&2
  exit 2
fi

# Try docker
if command -v docker >/dev/null 2>&1; then
  echo "Usando Docker mermaid-cli to generate PDF..."
  docker run --rm -v "$(pwd)":/data minlag/mermaid-cli -i /data/$INPUT -o /data/$OUTPDF || true
  if [ -f "$OUTPDF" ]; then
    echo "PDF generado: $OUTPDF"
    exit 0
  fi
fi

# Try npx
if command -v npx >/dev/null 2>&1; then
  echo "Usando npx @mermaid-js/mermaid-cli..."
  npx @mermaid-js/mermaid-cli -i "$INPUT" -o "$OUTPDF" --pdf && { echo "PDF generado: $OUTPDF"; exit 0; } || true
fi

# Try mmdc if installed
if command -v mmdc >/dev/null 2>&1; then
  echo "Usando mmdc local..."
  mmdc -i "$INPUT" -o "$OUTPDF" && { echo "PDF generado: $OUTPDF"; exit 0; } || true
fi

echo "No se pudo generar PDF automáticamente. Instala Docker, mmdc o usa: npm i -g @mermaid-js/mermaid-cli" >&2
exit 1
