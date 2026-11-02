#!/bin/bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

HOST="$(tr '[:lower:]' '[:upper:]' </etc/hostname | tr -d '[:space:]')"
case "$HOST" in
    THEMIS)
        playbook="playbooks/personal/server.yml"
        ;;
    ASTER | YUGEN | KVM)
        playbook="playbooks/personal/workstation.yml"
        ;;
    *)
        echo "hermes.sh: unknown host '$HOST' (expected ASTER, YUGEN, KVM, or THEMIS)" >&2
        exit 1
        ;;
esac

exec ansible-playbook "$playbook" \
    -i inventories/personal/hosts.yml \
    --tags hermes \
    --ask-vault-pass
