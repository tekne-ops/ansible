# Gaming Role

Installs gaming packages (Steam, Lutris, Wine, etc.) and configures a game launcher script for running games in a dedicated X session.

## What It Does

1. **Installs gaming packages** (Steam, Lutris, Wine, gamemode, MangoHud, gamescope)
2. **On `gaming_xorg_hosts`** copies the NVIDIA game-session config to `/etc/X11/yugen-game.conf` and removes the old `/etc/X11/xorg.conf.d/20-yugen-nvidia.conf` drop-in
3. **Copies** limits, schedtoold, gamemode, ntsync, and `/usr/local/bin/game`
4. **Publishes** Wine, NTSync, NVAPI, and the NVIDIA shader-cache variables to `/etc/environment` and `/etc/profile.d/gaming-performance.sh`
5. **Verifies** packages and deployed files

## Requirements

- `community.general` collection (for `pacman` module)

```bash
ansible-galaxy collection install community.general
```

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `gaming_packages` | See defaults | List of gaming packages |
| `gaming_xorg_conf_dest` | `/etc/X11/yugen-game.conf` | Game-session Xorg config, passed to `-xf86config` |
| `gaming_limits_conf_dest` | `/etc/security/limits.d/gaming.conf` | `@audio` and `@gamemode` limits |
| `gaming_script_dest` | `/usr/local/bin/game` | Dedicated X session launcher |
| `gaming_environment` | See defaults | Wine, NTSync, NVAPI, and shader-cache variables |

### Packages Installed

**Game launchers:** lutris, steam, gamescope

**Wine stack:** wine-tkg-valve-exp-bleeding, winetricks, wine-gecko, wine-mono, proton-ge-custom-bin

**Session and overlays:** openbox, gamemode, lib32-gamemode, mangohud, lib32-mangohud

**Fonts and libraries:** noto-fonts-cjk, lib32-systemd

## Files Deployed

| Source | Destination | Mode |
|--------|-------------|------|
| `files/game.conf` | `/etc/X11/yugen-game.conf` | 0644 |
| `files/gaming-limits.conf` | `/etc/security/limits.d/gaming.conf` | 0644 |
| `files/game` | `/usr/local/bin/game` | 0755 |
| `files/gamemode.ini` | `/etc/gamemode.ini` | 0644 |
| `files/schedtoold.conf` | `/etc/schedtoold.conf` | 0644 |

## Game Script Usage

The `game` script launches games in a dedicated X session:

```bash
game steam
game lutris
```

## Example Playbook

```yaml
- hosts: gaming-pc
  roles:
    - tekne.personal.gaming
```

## Tags

| Tag | Description |
|-----|-------------|
| `gaming` | All gaming tasks |
| `network` | Network connectivity wait (before packages) |
| `packages` | Package installation only |
| `config` | game.conf and game script deployment |
| `verify` | Verification tasks |

## License

MIT-0

## Author

dvaliente
