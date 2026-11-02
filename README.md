# ansible

One private Ansible repository for personal and professional automation. Personal and professional projects are separate collections, inventories, and playbooks. Shared host setup lives in a third collection that both sides can use.

## Layout

```
collections/ansible_collections/tekne/
  common/      shared host baseline
  personal/    desktop and homelab roles
  work/        Kubernetes and service-platform roles
inventories/personal/    workstations and THEMIS, including the encrypted vault
inventories/work/        Kubernetes cluster
playbooks/personal/      local personal entrypoints
playbooks/work/          work entrypoints
install/                 Arch installer
scripts/vault-pass-client.sh
```

`tekne.common` does not depend on the other two collections. `tekne.personal` and `tekne.work` depend on `tekne.common` and do not depend on each other. The personal server playbook calls `tekne.work` roles for THEMIS.

There is no default inventory. Every run passes `-i`.

## Run

Install third-party collections once. They go into `.ansible/collections`, which is not committed.

```bash
ansible-galaxy collection install -r requirements.yml
```

Personal workstation:

```bash
ansible-playbook playbooks/personal/workstation.yml \
  -i inventories/personal/hosts.yml \
  --ask-vault-pass
```

Personal server (THEMIS):

```bash
./playbooks/personal/server.sh
```

Work Kubernetes nodes:

```bash
ansible-playbook playbooks/work/k8s.yml -i inventories/work/hosts.yml
```

`./playbooks/personal/workstation.sh` reads the host profile in `install/profiles/hosts.json` and selects the playbook, inventory, and tags.

## Vault

Encrypted secrets for personal hosts are in `inventories/personal/group_vars/all/vault.yml`. Ansible loads that file with the inventory, so a personal run needs the vault password even for a single tag. The password is not stored in this repository.

`scripts/vault-pass-client.sh` reads `ansible/vault/personal` or `ansible/vault/work` from `pass` and refuses any other source. The committed vault has no vault-id label, and `ansible.cfg` does not call the script yet. After re-keying with `--encrypt-vault-id personal`, point `vault_identity_list` at the script.

There is no work vault until work secrets exist. Do not add them to the personal vault.

## Installer

From the repo root on a live ISO:

```bash
./install/arch-install.sh --vault-password-file ~/.vault_pass ASTER
```

The installer copies this checkout into the target. It does not clone a second collections repository.
