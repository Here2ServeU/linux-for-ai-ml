#!/usr/bin/env bash
# Course health check. Every line should say OK.
#   bash setup/doctor.sh

pass=0; fail=0
ok()   { echo "  [OK]   $1"; pass=$((pass + 1)); }
bad()  { echo "  [FAIL] $1"; shift; for f in "$@"; do echo "         fix: $f"; done; fail=$((fail + 1)); }
info() { echo "  [INFO] $1"; }

echo "Linux for AI-ML Systems · doctor"
echo

os=$(uname -s)

# How to install a package on this machine (used in the fix hints below).
install="sudo apt update && sudo apt install -y"
py_pkg="python3"
if [ "$os" = "Linux" ]; then
  if   command -v apt-get >/dev/null 2>&1; then install="sudo apt update && sudo apt install -y"
  elif command -v dnf     >/dev/null 2>&1; then install="sudo dnf install -y"
  elif command -v pacman  >/dev/null 2>&1; then install="sudo pacman -S --needed"; py_pkg="python"
  elif command -v zypper  >/dev/null 2>&1; then install="sudo zypper install -y"
  elif command -v apk     >/dev/null 2>&1; then install="sudo apk add"
  fi
elif [ "$os" = "Darwin" ]; then
  install="brew install"
fi

# 1. Linux
case "$os" in
  Linux)
    distro=$( (. /etc/os-release 2>/dev/null && echo "$PRETTY_NAME") || echo "Linux")
    if grep -qi microsoft /proc/version 2>/dev/null; then
      ok "Linux shell ($distro on WSL)"
      case "$PWD" in
        /mnt/[a-z]/*) info "you're on the Windows drive ($PWD). Labs run faster in your Linux home: cd ~ and clone there" ;;
      esac
    else
      ok "Linux shell ($distro)"
    fi
    ;;
  Darwin)
    if command -v multipass >/dev/null 2>&1; then
      if multipass info ailab >/dev/null 2>&1; then
        mac_fix="your Linux VM already exists. Enter it with:  multipass shell ailab"
      else
        mac_fix="Multipass is installed. Create your Linux VM:  multipass launch 24.04 --name ailab && multipass shell ailab"
      fi
    else
      mac_fix="install Multipass, then create a Linux VM:  brew install --cask multipass && multipass launch 24.04 --name ailab && multipass shell ailab"
    fi
    bad "Linux shell (found macOS, which is not Linux: its sed, du and find behave differently)" \
        "$mac_fix" \
        "then clone the repo inside the VM and run the doctor again. Full guide: setup/mac.md"
    ;;
  MINGW*|MSYS*|CYGWIN*)
    bad "Linux shell (found $os: this is Git Bash/Cygwin on Windows, not Linux)" \
        "in PowerShell (Admin):  wsl --install -d Ubuntu-24.04   then restart and open Ubuntu from the Start menu" \
        "full guide: setup/windows.md"
    ;;
  *)
    bad "Linux shell (found $os)" \
        "use GitHub Codespaces in your browser. Guide: setup/codespaces.md"
    ;;
esac

# 2. Python 3.9+
if command -v python3 >/dev/null 2>&1 && python3 -c 'import sys; sys.exit(sys.version_info < (3, 9))'; then
  ok "Python $(python3 -c 'import platform; print(platform.python_version())')"
else
  bad "Python 3.9 or newer" "$install $py_pkg"
fi

# 3. Git
if command -v git >/dev/null 2>&1; then
  ok "$(git --version)"
else
  bad "Git" "$install git"
fi

# 4. Core tools used in the labs
missing=""
for t in du df find grep sed sort head sha256sum stat ps pgrep; do
  command -v "$t" >/dev/null 2>&1 || missing="$missing $t"
done
if [ -z "$missing" ]; then ok "core tools (du df find grep sed sort head sha256sum stat ps pgrep)"
else bad "core tools, missing:$missing" "$install coreutils findutils grep sed procps"; fi

# 5. Free disk in $HOME (labs need about 1 GB)
free_kb=$(df -Pk "$HOME" | awk 'NR==2 {print $4}')
if [ "${free_kb:-0}" -ge 1048576 ]; then
  ok "free disk in \$HOME: $((free_kb / 1024 / 1024)) GB"
else
  bad "free disk in \$HOME: $((free_kb / 1024)) MB (need 1 GB)" "du -sh ~/* | sort -h, then clean up the biggest thing"
fi

# Optional: GPU (not needed for Modules 1-3)
if command -v nvidia-smi >/dev/null 2>&1; then
  info "GPU: $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null | head -1)"
else
  info "no NVIDIA GPU found (fine: Modules 1-3 run on CPU)"
fi

echo
if [ "$fail" -eq 0 ]; then
  echo "All $pass checks OK. You're ready."
else
  echo "$fail check(s) failed. Fix them, then run the doctor again."
  echo "Stuck for 15 minutes? Switch to GitHub Codespaces (setup/codespaces.md)."
  exit 1
fi
