#!/usr/bin/env bash
# Module 2 grader. Run it from inside ~/ai-job:
#   bash check_answers.sh <scratch-folder> <unreadable-file> <file-with-secret>
# Answers are stored as sha256 fingerprints, so reading this file won't spoil them.

if [ "$#" -ne 3 ]; then
  echo "Usage: bash check_answers.sh <scratch-folder> <unreadable-file> <file-with-secret>"
  echo "Example shape: bash check_answers.sh scratch/something datasets/x.jsonl configs/y.yaml"
  exit 2
fi

# Turn "./scratch/run/" into "scratch/run" so small style differences don't cost points.
norm() { local p="${1#./}"; p="${p%/}"; printf '%s' "$p"; }
fp()   { printf '%s' "$1" | sha256sum | cut -c1-16; }

A1=72bd50e9a4d06dab  # mission 1
A2=5190b0f6e578c7de  # mission 2
A3=dbb61971a1775b7e  # mission 3

score=0
check() {  # name, given, expected-fingerprint, hint
  if [ "$(fp "$(norm "$2")")" = "$3" ]; then
    echo "  [OK]   $1"; score=$((score + 1))
  else
    echo "  [MISS] $1  -> $4"
  fi
}

echo "Checking your findings..."
check "Mission 1 · Disk"        "$1" "$A1" "try: du -sh scratch/* | sort -h  (biggest is last)"
check "Mission 2 · Permissions" "$2" "$A2" "try: ls -l datasets  (look for a missing r)"
check "Mission 3 · Secrets"     "$3" "$A3" "try: grep -rn token configs"

echo
echo "Score: $score / 3"

# Did you also fix things? (Not scored, but this is the real job.)
echo
if [ -f preflight.sh ] && bash preflight.sh >/dev/null 2>&1; then
  echo "  Fix check: preflight.sh says GO. Run-08 is safe to start."
  go=1
else
  echo "  Fix check: preflight.sh still says NO-GO. Run it to see what's left:  bash preflight.sh"
  go=0
fi

if [ "$score" -eq 3 ] && [ "$go" -eq 1 ]; then
  echo
  echo "You just stopped a training run from dying at 97%."
fi
