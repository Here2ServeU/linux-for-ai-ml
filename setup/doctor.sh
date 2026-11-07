#!/usr/bin/env bash
# Course health check. Every line should say OK.
#   bash setup/doctor.sh

pass=0; fail=0
ok()   { echo "  [OK]   $1"; pass=$((pass + 1)); }
bad()  { echo "  [FAIL] $1"; echo "         fix: $2"; fail=$((fail + 1)); }
info() { echo "  [INFO] $1"; }

echo "Linux for AI-ML Systems · doctor"
echo

# 1. Linux
if [ "$(uname -s)" = "Linux" ]; then
  distro=$( (. /etc/os-release 2>/dev/null && echo "$PRETTY_NAME") || echo "Linux")
  ok "Linux shell ($distro)"
else
  bad "Linux shell (found $(uname -s))" "use Codespaces, WSL (Windows) or Multipass (Mac). See setup/README.md"
fi

# 2. Python 3.9+
if command -v python3 >/dev/null 2>&1 && python3 -c 'import sys; sys.exit(sys.version_info < (3, 9))'; then
  ok "Python $(python3 -c 'import platform; print(platform.python_version())')"
else
  bad "Python 3.9 or newer" "sudo apt update && sudo apt install -y python3"
fi

# 3. Git
if command -v git >/dev/null 2>&1; then
  ok "$(git --version)"
else
  bad "Git" "sudo apt update && sudo apt install -y git"
fi

# 4. Core tools used in the labs
missing=""
for t in du df find grep sed sort head sha256sum; do
  command -v "$t" >/dev/null 2>&1 || missing="$missing $t"
done
if [ -z "$missing" ]; then ok "core tools (du df find grep sed sort head sha256sum)"
else bad "core tools, missing:$missing" "sudo apt install -y coreutils findutils grep sed"; fi

# 5. Free disk in $HOME (labs need about 1 GB)
free_kb=$(df -Pk "$HOME" | awk 'NR==2 {print $4}')
if [ "${free_kb:-0}" -ge 1048576 ]; then
  ok "free disk in \$HOME: $((free_kb / 1024 / 1024)) GB"
else
  bad "free disk in \$HOME: $((free_kb / 1024)) MB (need 1 GB)" "du -sh ~/* | sort -h, then clean up the biggest thing"
fi

# Optional: GPU (not needed for Module 1)
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
  echo "Stuck for 15 minutes? Switch to GitHub Codespaces."
  exit 1
fi
