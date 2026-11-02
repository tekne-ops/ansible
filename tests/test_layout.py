"""Layout and boundary checks. These tests do not decrypt the vault."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COLLECTIONS = ROOT / "collections" / "ansible_collections" / "tekne"

COMMON = {"user", "hostname", "network", "os", "nftables", "docker", "libvirt"}
PERSONAL = {
    "bootstrap",
    "gaming",
    "gpu",
    "kde",
    "xfce4",
    "pipewire",
    "onedrive",
    "gerbera",
    "repotekne",
    "hermes",
    "n8n",
}
WORK = {"k8s", "consul", "jenkins", "haproxy"}
EXPECTED = {"common": COMMON, "personal": PERSONAL, "work": WORK}

ROLE_FQCN = re.compile(r"tekne\.(common|personal|work)\.[a-z0-9_]+")
TEXT_SUFFIXES = {".yml", ".yaml", ".md", ".j2", ".py"}


def collection_roles(name: str) -> set[str]:
    roles = COLLECTIONS / name / "roles"
    return {path.name for path in roles.iterdir() if path.is_dir()}


def read_texts(root: Path) -> list[tuple[Path, str]]:
    files = []
    for path in root.rglob("*"):
        if path.is_file() and path.suffix in TEXT_SUFFIXES and ".git" not in path.parts:
            files.append((path, path.read_text(encoding="utf-8")))
    return files


class LayoutTest(unittest.TestCase):
    def test_each_role_lives_in_one_collection(self) -> None:
        for name, roles in EXPECTED.items():
            self.assertEqual(collection_roles(name), roles)

    def test_personal_vault_is_encrypted(self) -> None:
        vault = ROOT / "inventories/personal/group_vars/all/vault.yml"
        lines = vault.read_text(encoding="utf-8").splitlines()
        self.assertTrue(lines[0].startswith("$ANSIBLE_VAULT;"))
        for line in lines[1:]:
            self.assertRegex(line, r"^[0-9a-f]+$")

    def test_work_inventory_has_no_vault_file(self) -> None:
        work = ROOT / "inventories/work"
        vaults = [path for path in work.rglob("*") if path.name == "vault.yml"]
        self.assertEqual(vaults, [])

    def test_no_retired_collection_name_in_runtime_files(self) -> None:
        roots = [
            COLLECTIONS,
            ROOT / "playbooks",
            ROOT / "install",
        ]
        for root in roots:
            for path, text in read_texts(root):
                if path.parts[-2:] == ("changelogs", "changelog.yaml"):
                    continue
                self.assertNotIn("tekne.devops", text, str(path.relative_to(ROOT)))

    def test_collections_do_not_cross_boundaries(self) -> None:
        forbidden = {
            "common": {"personal", "work"},
            "personal": {"work"},
            "work": {"personal"},
        }
        for name, blocked in forbidden.items():
            for path, text in read_texts(COLLECTIONS / name):
                for match in ROLE_FQCN.finditer(text):
                    self.assertNotIn(
                        match.group(1),
                        blocked,
                        f"{path.relative_to(ROOT)} references {match.group(0)}",
                    )

    def test_galaxy_dependencies_do_not_cross_boundaries(self) -> None:
        for name, blocked in {"common": {"personal", "work"}, "personal": {"work"}, "work": {"personal"}}.items():
            text = (COLLECTIONS / name / "galaxy.yml").read_text(encoding="utf-8")
            for other in blocked:
                self.assertNotIn(f"tekne.{other}:", text)

    def test_work_playbooks_do_not_call_personal_roles(self) -> None:
        for path, text in read_texts(ROOT / "playbooks/work"):
            for match in ROLE_FQCN.finditer(text):
                self.assertNotEqual(match.group(1), "personal", str(path.relative_to(ROOT)))

    def test_personal_playbook_may_call_work_roles(self) -> None:
        text = (ROOT / "playbooks/personal/tasks/server_roles.yml").read_text(encoding="utf-8")
        self.assertIn("tekne.work.haproxy", text)
        self.assertIn("tekne.common.user", text)


if __name__ == "__main__":
    unittest.main()
