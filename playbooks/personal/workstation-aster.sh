#!/bin/bash
set -euo pipefail

HOST="$(tr '[:lower:]' '[:upper:]' </etc/hostname | tr -d '[:space:]')"
if [[ "$HOST" != ASTER ]]; then
    echo "workstation-aster.sh: this playbook is for ASTER (current host: ${HOST})" >&2
    exit 1
fi

exec "$(dirname "$0")/workstation.sh" "$@"
