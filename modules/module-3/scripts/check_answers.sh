#!/usr/bin/env bash
# Module 3 grader. Run it from inside ~/ai-lab:
#   bash check_answers.sh <cpu-program> <memory-program> <llm-serve-pid>
# Answers are stored as sha256 fingerprints, so reading this file won't spoil them.

if [ "$#" -ne 3 ]; then
  echo "Usage: bash check_answers.sh <cpu-program> <memory-program> <llm-serve-pid>"
  echo "Example shape: bash check_answers.sh some-name other-name 12345"
  exit 2
fi
if [ ! -f .lab-state ]; then
  echo "Run this from inside the lab folder:  cd ~/ai-lab && bash check_answers.sh ..."
  exit 2
fi

here=$(pwd -P)

# Accept "data-loader", "./bin/data-loader" or "Data-Loader".
norm() { local p="${1%/}"; p="${p##*/}"; printf '%s' "$p" | tr 'A-Z' 'a-z'; }
fp()   { printf '%s' "$1" | sha256sum | cut -c1-16; }
pid_of() { awk -F= -v n="$1" '$1 == n {print $2}' .lab-state; }
# Running = the PID exists AND is still our lab program (PIDs get reused).
running() {
  local pid; pid=$(pid_of "$1")
  [ -r "/proc/$pid/cmdline" ] && tr '\0' ' ' < "/proc/$pid/cmdline" | grep -q "$here/bin/$1"
}

A1=fb9d70615dfb8f41  # mission 1
A2=8102c99f9294ab84  # mission 2

score=0
check() {  # name, ok?, hint
  if [ "$2" = yes ]; then
    echo "  [OK]   $1"; score=$((score + 1))
  else
    echo "  [MISS] $1  -> $3"
  fi
}
is() { [ "$1" = "$2" ] && echo yes || echo no; }

echo "Checking your findings..."
check "Mission 1 · CPU"    "$(is "$(fp "$(norm "$1")")" "$A1")" "try: ps aux --sort=-%cpu | head -5   (or top, then P)"
check "Mission 2 · Memory" "$(is "$(fp "$(norm "$2")")" "$A2")" "try: ps aux --sort=-%mem | head -5   (or top, then M)"
check "Mission 3 · Server" "$(is "$3" "$(pid_of llm-serve)")"   "try: pgrep llm-serve   (or ps aux | grep llm-serve)"

echo
echo "Score: $score / 3"

# Did you also fix things? (Not scored, but this is the real job.)
fixed=0
echo
if running data-loader; then
  echo "  Fix check: data-loader is still burning CPU. Stop it:  kill <pid>"
else
  echo "  Fix check: data-loader stopped. CPU is free."; fixed=$((fixed + 1))
fi
if running cache-warmer; then
  echo "  Fix check: cache-warmer still holds its memory. Did it ignore kill? Check logs/cache-warmer.log"
else
  echo "  Fix check: cache-warmer stopped. Memory is back."; fixed=$((fixed + 1))
fi
if running llm-serve; then
  echo "  Fix check: llm-serve is still running. Users are being served."; fixed=$((fixed + 1))
else
  echo "  Fix check: llm-serve is DOWN. You stopped the model server!"
  echo "             Start over:  cd ~/linux-for-ai-ml/modules/module-3/scripts && python3 make_lab.py --reset"
fi

if [ "$score" -eq 3 ] && [ "$fixed" -eq 3 ]; then
  echo
  echo "You just rescued a server without taking the model down."
fi
