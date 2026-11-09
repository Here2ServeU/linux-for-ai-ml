#!/usr/bin/env bash
# Module 2 pre-flight: GO / NO-GO before a training job starts.
# Run it from inside the job folder (~/ai-job):
#   bash preflight.sh
# Three checks: disk, permissions, secrets. Any FAIL means NO-GO.

cfg=configs/train.yaml
if [ ! -f "$cfg" ]; then
  echo "No $cfg here. Run this from inside the job folder:  cd ~/ai-job && bash preflight.sh"
  exit 2
fi

fails=0
ok()  { echo "  [OK]   $1"; }
bad() { echo "  [FAIL] $1"; echo "         $2"; fails=$((fails + 1)); }
val() { awk -v k="$1:" '$1 == k {print $2}' "$cfg"; }

echo "Pre-flight for $(basename "$PWD")"
echo

# 1. Disk: will the run fit?
need=$(val needs_scratch_mb)
quota=$(val scratch_quota_mb)
scratch=$(val scratch_dir)
used=$(du -sm "$scratch" 2>/dev/null | cut -f1)
left=$((quota - ${used:-0}))
free=$(df -Pm . | awk 'NR==2 {print $4}')
if [ "$free" -lt "$need" ]; then
  bad "Disk: only ${free} MB free on this disk, the run needs ${need} MB" \
      "look with:  df -h .   then  du -sh ~/* | sort -h"
elif [ "$left" -lt "$need" ]; then
  bad "Disk: scratch has ${left} MB left of its ${quota} MB quota, the run needs ${need} MB" \
      "look with:  du -sh $scratch/* | sort -h"
else
  ok "Disk: scratch has ${left} MB left, the run needs ${need} MB"
fi

# 2. Permissions: can the job read its data?
for key in dataset eval_dataset; do
  f=$(val "$key")
  [ -z "$f" ] && continue
  if [ ! -e "$f" ]; then
    bad "Permissions: $f doesn't exist" "check the path in $cfg"
  elif [ "$(stat -c %A "$f" | cut -c2)" != "r" ]; then
    bad "Permissions: $f is $(stat -c %A "$f"), the job can't read it" \
        "look with:  ls -l $(dirname "$f")"
  else
    ok "Permissions: $f is readable ($(stat -c %A "$f"))"
  fi
done

# 3. Secrets: no tokens in configs, and the job can still get its token.
leaks=$(grep -rlE '(hf_|sk-)[A-Za-z0-9_]{20,}' configs 2>/dev/null)
if [ -n "$leaks" ]; then
  bad "Secrets: a token is pasted into $(echo $leaks)" \
      "configs get shared and committed. Move the token into .env"
elif [ -f .env ] && [ "$(stat -c %a .env)" != "600" ]; then
  bad "Secrets: .env is $(stat -c %A .env), so other users can read it" \
      "lock it down:  chmod 600 .env"
elif [ -n "${HF_TOKEN:-}" ] || grep -qs '^HF_TOKEN=' .env; then
  ok "Secrets: no tokens in configs, HF_TOKEN comes from $( [ -n "${HF_TOKEN:-}" ] && echo 'the environment' || echo '.env (600)')"
else
  bad "Secrets: no tokens in configs, but the job has no HF_TOKEN either" \
      "put it in .env:  echo 'HF_TOKEN=...' > .env && chmod 600 .env"
fi

echo
if [ "$fails" -eq 0 ]; then
  echo "GO: all pre-flight checks passed. Safe to start the run."
else
  echo "NO-GO: $fails check(s) failed. Fix them before you start the run."
  exit 1
fi
