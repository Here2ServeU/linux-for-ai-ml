# Already on Linux

Use your normal terminal. The course is tested on **Ubuntu 24.04**, and any
recent distro should work.

## Install Git and Python 3.9+ (skip what you already have)

| Distro | Command |
|---|---|
| Ubuntu / Debian / Mint / Pop!_OS | `sudo apt update && sudo apt install -y git python3` |
| Fedora / RHEL / Rocky / Alma | `sudo dnf install -y git python3` |
| Arch / Manjaro | `sudo pacman -S --needed git python` |
| openSUSE | `sudo zypper install -y git python3` |
| Alpine | `sudo apk add git python3 bash coreutils findutils` |

## Get the course

```bash
git clone https://github.com/Here2ServeU/linux-for-ai-ml
cd linux-for-ai-ml && bash setup/doctor.sh
```

## Also works

- **A cloud VM or work server** (AWS, GCP, Azure, a lab box): SSH in and follow
  the same steps. The labs only write to `~/ai-server`.
- **Raspberry Pi** (Raspberry Pi OS 64-bit): use the Ubuntu/Debian row above.

Note: on Alpine and other minimal images, install `bash`. The scripts use it.
