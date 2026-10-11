#!/bin/sh
set -eu
# Render supplies the HTTPS service address and listening port.
# No credentials are created or printed during deployment.
if [ -n "${RENDER_EXTERNAL_URL:-}" ]; then
    export ESCRIBANIA_MODE=production
    export ESCRIBANIA_ORIGIN="${ESCRIBANIA_ORIGIN:-$RENDER_EXTERNAL_URL}"
fi
exec python -m uvicorn app:app --host 0.0.0.0 --port "${PORT:-8001}" --workers 1 --no-access-log
