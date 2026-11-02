# Playbooks

Personal entrypoints run against `inventories/personal`. Work entrypoints run against `inventories/work`. Each playbook asserts `tekne_context` before it changes anything.

| Playbook | Inventory | Hosts |
|---|---|---|
| `personal/workstation.yml` | `inventories/personal` | ASTER, YUGEN, KVM |
| `personal/server.yml` | `inventories/personal` | THEMIS |
| `personal/main.yml` | `inventories/personal` | dispatcher for the four personal hosts |
| `personal/onedrive-auth.yml` | `inventories/personal` | interactive OneDrive login |
| `work/k8s.yml` | `inventories/work` | Kubernetes nodes |

Host profiles for the personal machines are `inventories/personal/host_vars/<HOSTNAME>.yml`. The hostname task loads the file that matches `/etc/hostname`.
