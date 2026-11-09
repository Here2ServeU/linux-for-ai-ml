# Module 2 · Feed the Model

**Core idea:** most training jobs that die at 97% died before they started.
Disk, permissions and secrets: a three-part pre-flight check stops that.

**Memory hook:** Will it fit? Can it read? Is it secret?

~45 min · 4 sections · 1 lab

| # | Section | Time | The one idea |
|:-:|---|:-:|---|
| 01 | Will It Fit? | ~8 min | `df -h` + `du -sh` before every download or training run (reuses Module 1). |
| 02 | Who Can Read It? | ~10 min | Owners, groups and `rwx`: `ls -l`, `chmod`, `chown`. |
| 03 | Keep Secrets Secret | ~10 min | API keys and tokens: environment variables, `.env`, `chmod 600`, never in Git. |
| 04 | Build It: The Pre-Flight Script | ~12 min | One script that says GO / NO-GO before a job starts. |

---

## The lab: a pre-flight check before run-08

### Step 1 · Get the lab

Already did Module 1? You have the repo; just update it:

```bash
cd ~/linux-for-ai-ml && git pull && bash setup/doctor.sh
```

New here? Follow Step 1 in [Module 1](../module-1/README.md#step-1--get-the-lab-check-your-machine) first.

### Step 2 · Build the training job

```bash
cd ~/linux-for-ai-ml/modules/module-2/scripts && python3 make_job.py
cd ~/ai-job && cat README-FIRST.txt
```

This builds a small fine-tuning job in your home folder: a dataset, scratch
space for checkpoints, configs and the log of last night's run, which died at 97%.
Run-08 is next, and it will fail too. Your three missions:

1. **Disk** — Will it fit? What is filling the scratch space?
2. **Permissions** — Which file can the job not read?
3. **Secrets** — Which file has a secret pasted into it?

Ask the pre-flight script first. It tells you *that* something is wrong, not *why*:

```bash
bash preflight.sh
```

```
  [FAIL] Disk: scratch has 7 MB left of its 40 MB quota, the run needs 20 MB
  [FAIL] Permissions: datasets/train.jsonl is --w-------, the job can't read it
  [OK]   Permissions: datasets/eval.jsonl is readable (-rw-r--r--)
  [FAIL] Secrets: a token is pasted into configs/train.yaml

NO-GO: 3 check(s) failed. Fix them before you start the run.
```

Try the missions yourself first. The walkthrough is below.

<details>
<summary><b>Step 3 · Mission 1: will it fit?</b></summary>

```bash
grep -rn ERROR logs
df -h .
du -sh scratch/* | sort -h
```

```
logs/run-07.log:6:... ERROR No space left on device: scratch/run-07/step-9700.pt
516K  scratch/cache
2.1M  scratch/run-07
31M   scratch/run-03-tmp
```

The disk itself has room (`df -h`), but this job may only use 40 MB of scratch,
and `run-03-tmp` (temp shards from an old run) takes 31 MB of it. Run-08 needs 20 MB.
Check nothing points at it, then remove it:

```bash
grep -rn run-03 configs     # nothing uses it
rm -r scratch/run-03-tmp
```
</details>

<details>
<summary><b>Step 4 · Mission 2: who can read it?</b></summary>

```bash
ls -l datasets
```

```
-rw-r--r-- 1 you you  614400 ... eval.jsonl
--w------- 1 you you 6291456 ... train.jsonl
```

`--w-------`: the owner can write, but nobody can **r**ead. The job would open
the file and crash. Give the owner read and write, everyone else read:

```bash
chmod 644 datasets/train.jsonl
ls -l datasets/train.jsonl     # -rw-r--r--
```

On a shared server the file might belong to someone else. Then `ls -l` shows
another owner, and the fix is `sudo chown you:you file` instead.
</details>

<details>
<summary><b>Step 5 · Mission 3: keep secrets secret</b></summary>

```bash
grep -rn token configs
```

```
configs/train.yaml:9:hf_token: hf_LABfakeToken...
```

Configs get shared, copied and committed to Git. A token in a config is a
token on the internet. Move it into `.env`, which `.gitignore` already keeps out of Git,
and make it readable by you only:

```bash
grep hf_token configs/train.yaml | sed 's/hf_token: /HF_TOKEN=/' > .env
sed -i '/^hf_token:/d' configs/train.yaml
chmod 600 .env
ls -l .env          # -rw-------
cat .gitignore      # .env is listed
```

Prefer an environment variable? `export HF_TOKEN=...` works too: the pre-flight
accepts either. Just `unset HF_TOKEN` when you're done.

⚠️ On a real project, a token that ever reached Git is burned. Removing it from
the file isn't enough: revoke it and make a new one.
</details>

<details>
<summary><b>Step 6 · Pre-flight again, then check your answers</b></summary>

```bash
bash preflight.sh
bash check_answers.sh scratch/run-03-tmp datasets/train.jsonl configs/train.yaml
```

```
GO: all pre-flight checks passed. Safe to start the run.

Score: 3 / 3
  Fix check: preflight.sh says GO. Run-08 is safe to start.
You just stopped a training run from dying at 97%.
```
</details>

### Section 04 · Build it: read the pre-flight script

`preflight.sh` is about 70 lines of plain Bash, and every check uses a command
from this module: `df` and `du` for disk, `stat` for permissions, `grep` for
secrets. Read it, then make it yours:

```bash
less preflight.sh
```

Challenge: add a fourth check that fails if `scratch/` holds any `*.tmp` file
older than 7 days (`find scratch -name '*.tmp' -mtime +7`).

### Practice again

```bash
cd ~/linux-for-ai-ml/modules/module-2/scripts && python3 make_job.py --reset
```

Goal: from NO-GO to GO in under 5 minutes.

### Clean up

Done with the lab? Remove the practice job (about 40 MB), and clear any
token you exported:

```bash
cd ~/linux-for-ai-ml/modules/module-2/scripts && python3 make_job.py --clean
unset HF_TOKEN
```

It only deletes a folder the lab built, and refuses anything else. Built it
somewhere else with `--dir`? Pass the same `--dir` to `--clean`.

---

## Exercises (before Module 3)

1. **Free space** — `df -h ~` on your machine. How many GB are free?
2. **Read the bits** — `ls -l /etc/passwd /etc/shadow`. Why can you read one but not the other?
3. **Break & fix** — `touch x; chmod 000 x; cat x`, then fix it with `chmod 644 x`.
4. **Octal** — write `rwxr-x---` as a number. (Answer: 750.)
5. **Hunt secrets** — after your fix, `grep -rnE '(hf_|sk-)[A-Za-z0-9]{20,}' ~/ai-job/configs` finds nothing. Try it on your own projects too.
6. **Env vars** — `export DEMO=hi; echo $DEMO; unset DEMO; echo $DEMO`
7. **Break & fix** — `make_job.py --reset`, then reach GO again in 5 min.

**Self-check (from memory):** *A training run is about to start. What three things do you check first?*

<details><summary>Answer</summary>

Will it fit (`df -h`, `du -sh`)? Can it read its data (`ls -l`)? Are the secrets out of the configs (`grep`, `.env` with `chmod 600`)?
</details>

**Next:** Module 3 moves from *file at rest* to *process at work*.

---

📚 Part of **Linux for AI-ML Systems**, a T2S course. Subscribe at
**[transformed2succeed.com/membership](https://www.transformed2succeed.com/membership)** for access to all courses.
