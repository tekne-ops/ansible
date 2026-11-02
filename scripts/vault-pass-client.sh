#!/usr/bin/env bash
# Print an Ansible Vault password from the pass store. This script stores nothing.
#
#   pass insert ansible/vault/personal
#   pass insert ansible/vault/work
#
# The committed personal vault has no vault-id label. Re-key it before pointing
# ansible.cfg vault_identity_list at this script:
#
#   ansible-vault rekey --encrypt-vault-id personal inventories/personal/group_vars/all/vault.yml
#
# ansible.cfg does not call this script yet, so --ask-vault-pass still works.
set -euo pipefail

identity="${ANSIBLE_VAULT_IDENTITY:-personal}"
case "$identity" in
    personal | work | default) ;;
    *)
        echo "vault-pass-client: refusing unknown vault identity: ${identity}" >&2
        exit 1
        ;;
esac

if [[ "$identity" == "default" ]]; then
    identity="personal"
fi

if ! command -v pass >/dev/null 2>&1; then
    echo "vault-pass-client: pass is not installed. Refusing to read a password file." >&2
    exit 1
fi

exec pass show "ansible/vault/${identity}"
