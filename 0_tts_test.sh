#!/usr/bin/env bash
set -euo pipefail

echo "[1/5] Locate script dir"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
echo "SCRIPT_DIR=$SCRIPT_DIR"

echo "[2/5] Load .env"
if [[ ! -f "${SCRIPT_DIR}/.env" ]]; then
  echo "ERROR: ${SCRIPT_DIR}/.env not found" >&2
  exit 1
fi
set -a
source "${SCRIPT_DIR}/.env"
set +a

echo "[3/5] Check key"
: "${OPENAI_API_KEY:?OPENAI_API_KEY not set}"
echo "Key length: ${#OPENAI_API_KEY}"

echo "[4/5] Call TTS API"
curl -v -X POST "https://api.openai.com/v1/audio/speech" \
  -H "Authorization: Bearer ${OPENAI_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "Accept: audio/mpeg" \
  --fail-with-body \
  -d '{
    "model": "gpt-4o-mini-tts",
    "voice": "alloy",
    "input": "Hello world, this is my test for text to speech."
  }' \
  -D "${SCRIPT_DIR}/resp.headers" \
  -o "${SCRIPT_DIR}/hello.mp3"

echo "[5/5] Verify output"
ls -lh "${SCRIPT_DIR}/hello.mp3"
if command -v file >/dev/null 2>&1; then
  file "${SCRIPT_DIR}/hello.mp3" || true
else
  echo "First 4 bytes (expect ID3):"
  xxd -l 4 "${SCRIPT_DIR}/hello.mp3" || true
fi

echo "Done."
