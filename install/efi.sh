#!/bin/bash
set -euo pipefail

# efibootmgr --create --disk /dev/nvme0n1 --part 1 --create --label "BOOT" --loader "\\EFI\\Linux\\arch-linux-tkg-aster.efi" --unicode "root=LABEL=ROOT rw split_lock_detect=off nowatchdog mitigations=off quiet splash vt.global_cursor_default=0 loglevel=2 systemd.show_status=false rd.udev.log_level=2"
efibootmgr --create --disk /dev/nvme0n1 --part 1 --create --label "BOOT" --loader "\\EFI\\Linux\\arch-linux-tkg-aster.efi" --unicode
