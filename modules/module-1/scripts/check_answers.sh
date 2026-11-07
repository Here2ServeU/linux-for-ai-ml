#!/usr/bin/env bash
# Module 1 grader. Run it from inside ~/ai-server:
#   bash check_answers.sh <biggest-folder> <broken-config> <duplicate-file>
# Answers are stored as sha256 fingerprints, so reading this file won't spoil them.

if [ "$#" -ne 3 ]; then
  echo "Usage: bash check_answers.sh <biggest-folder> <broken-config> <duplicate-file>"
  echo "Example shape: bash check_answers.sh somefolder configs/x.yaml models/a/b.safetensors"
  exit 2
fi

# Turn "./models/" into "models" so small style differences don't cost points.
norm() { local p="${1#./}"; p="${p%/}"; printf '%s' "$p"; }
fp()   { printf '%s' "$1" | sha256sum | cut -c1-16; }

A1=8edcc26c0f6c7256  # mission 1
A2=7a4e87ed099c7a5d  # mission 2
A3=1ab5c80115777f59  # mission 3

score=0
check() {  # name, given, expected-fingerprint, hint
  if [ "$(fp "$(norm "$2")")" = "$3" ]; then
    echo "  [OK]   $1"; score=$((score + 1))
  else
    echo "  [MISS] $1  -> $4"
  fi
}

echo "Checking your findings..."
check "Mission 1 · Disk"      "$1" "$A1" "try: du -sh * | sort -h  (biggest is last)"
check "Mission 2 · Startup"   "$2" "$A2" "try: grep -rn ERROR logs, then grep -n model_path configs/*.yaml"
check "Mission 3 · Duplicate" "$3" "$A3" "try: find models -name '*.safetensors' -exec sha256sum {} +"

echo
echo "Score: $score / 3"

# Did you also fix things? (Not scored, but this is the real job.)
if [ -f configs/serve.yaml ]; then
  path=$(grep -E '^model_path:' configs/serve.yaml | awk '{print $2}')
  if [ -n "$path" ] && [ -f "$path" ]; then
    echo "  Fix check: serve.yaml now points at a file that exists."
  else
    echo "  Fix check: serve.yaml still points at '$path', which doesn't exist."
  fi
fi
if [ -d models/old ]; then
  echo "  Fix check: models/old is still there. Prove it's a copy, then remove it."
else
  echo "  Fix check: duplicate removed. Disk reclaimed."
fi

if [ "$score" -eq 3 ]; then
  echo
  echo "You just diagnosed a server you had never seen."
fi
