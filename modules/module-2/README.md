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

**Your materials:** this README is the lab guide.
[WORKBOOK.md](WORKBOOK.md) is where you write your answers as you go.
The slides are in [slides/](slides/) as a PDF: [Linux_AI_ML_Module_2_Student.pdf](slides/Linux_AI_ML_Module_2_Student.pdf).
All three follow the same steps in the same order.

---

## Before you start: how to read the commands

```bash
cd ~/ai-job   # go into the ai-job folder
```

| You see | What it means |
|---|---|
| `cd ~/ai-job` | Type exactly this, spaces included, then press **Enter**. |
| `# go into…` | A comment: a note for you. Don't type it. |
| `~` | Your home folder, e.g. `/home/ubuntu`. |
| `$` (on the slides) | The prompt Linux shows. Don't type it. |

Type **one line at a time**. Wait for the prompt to come back before typing the next line.
After each step, compare your screen with **You should see**. If they're different, check
[Stuck?](#stuck) at the end of this page.

---

## The lab: a pre-flight check before run-08

### Step 1 · Get the lab

Already did Module 1? You have the repo; just update it:

```bash
cd ~/linux-for-ai-ml        # go to the course repo
git pull                    # get the newest lab files
bash setup/doctor.sh        # check Linux, Python, Git and disk
```

**You should see:** every line says `OK`.

- On **Codespaces** the repo lives somewhere else: use `cd /workspaces/linux-for-ai-ml` instead.
- `cd` says `No such file or directory`? You don't have the repo yet. Follow Step 1 in
  [Module 1](../module-1/README.md#step-1--get-the-lab-check-your-machine) first.

### Step 2 · Build the training job

```bash
cd ~/linux-for-ai-ml/modules/module-2/scripts   # the Module 2 scripts
python3 make_job.py                              # builds ~/ai-job
cd ~/ai-job                                      # walk into the job
cat README-FIRST.txt                             # read the briefing
```

**You should see:**

```
Built your training job at /home/you/ai-job
Next:  cd /home/you/ai-job && cat README-FIRST.txt
Welcome to ai-job. Last night's run died at 97% after almost 6 hours.
...
```

Your home folder replaces `/home/you`. Got `already exists`? You built it before:
`python3 make_job.py --reset` rebuilds it fresh.

This builds a small fine-tuning job in your home folder. Look around with `ls`:

| Folder / file | What it is |
|---|---|
| `datasets/` | The training data: `train.jsonl` and `eval.jsonl` |
| `scratch/` | Where the job saves checkpoints. Its quota is 40 MB |
| `configs/` | Settings for the run: `train.yaml`, `eval.yaml` |
| `logs/` | The log of last night's run, which died at 97% |
| `preflight.sh` | The pre-flight check: says GO or NO-GO |
| `check_answers.sh` | Scores your three answers |

Sizes are scaled: 1 MB here stands for 1 GB on a real server. The token in this job is fake.

Run-08 is next, and it will fail too. Your three missions:

1. **Disk**: Will it fit? What is filling the scratch space?
2. **Permissions**: Which file can the job not read?
3. **Secrets**: Which file has a secret pasted into it?

Ask the pre-flight script first. It tells you *that* something is wrong, not *why*.
Run it from inside `~/ai-job`:

```bash
bash preflight.sh
```

**You should see** (NO-GO is expected here):

```
[FAIL] Disk: scratch has 7 MB left of its 40 MB quota, the run needs 20 MB
[FAIL] Permissions: datasets/train.jsonl is --w-------, the job can't read it
[OK]   Permissions: datasets/eval.jsonl is readable (-rw-r--r--)
[FAIL] Secrets: a token is pasted into configs/train.yaml

NO-GO: 3 check(s) failed. Fix them before you start the run.
```

Try the missions yourself first. The walkthrough is below: open one step at a time.

<details>
<summary><b>Step 3 · Mission 1: will it fit?</b></summary>

Find it:

```bash
cd ~/ai-job                    # make sure you're in the job
grep -rn ERROR logs            # what killed last night's run?
df -h .                        # is the disk itself full?
du -sh scratch/* | sort -h     # who is filling scratch? (biggest is last)
```

The `|` is the pipe key: **Shift + backslash**. **You should see:**

```
logs/run-07.log:6:... ERROR No space left on device: scratch/run-07/step-9700.pt
516K scratch/cache
2.1M scratch/run-07
31M scratch/run-03-tmp
```

The disk itself has room (`df -h` shows GBs free), but this job may only use 40 MB of scratch,
and `run-03-tmp` (temp shards from an old run) takes 31 MB of it. Run-08 needs 20 MB.

✏️ **Mission 1 answer:** `scratch/run-03-tmp`. Write it in your workbook.

Fix it. Check nothing points at it, then remove it:

```bash
grep -rn run-03 configs        # does any config use it? (no output = no)
rm -r scratch/run-03-tmp       # delete the folder. rm has no undo
bash preflight.sh              # check again
```

**You should see:** `[OK] Disk: scratch has 37 MB left, the run needs 20 MB`. Two FAILs remain.
</details>

<details>
<summary><b>Step 4 · Mission 2: who can read it?</b></summary>

```bash
ls -l datasets                 # look for a missing r
```

**You should see:**

```
-rw-r--r-- 1 you you 614400 ... eval.jsonl
--w------- 1 you you 6291456 ... train.jsonl
```

Read the ten characters as type · owner · group · others. `--w-------`: the owner can write,
but nobody can **r**ead. The job would open the file and crash.

✏️ **Mission 2 answer:** `datasets/train.jsonl`

Give the owner read and write, everyone else read (r=4, w=2, x=1, so `rw-r--r--` = 644):

```bash
chmod 644 datasets/train.jsonl
ls -l datasets/train.jsonl     # -rw-r--r--
bash preflight.sh              # check again
```

**You should see:** `[OK] Permissions: datasets/train.jsonl is readable (-rw-r--r--)`. One FAIL remains.

Never use `chmod 777`: it makes errors go away by removing all protection.
On a shared server the file might belong to someone else. Then `ls -l` shows
another owner, and the fix is `sudo chown you:you file` instead.
</details>

<details>
<summary><b>Step 5 · Mission 3: keep secrets secret</b></summary>

```bash
grep -rn token configs         # search every config for "token"
```

**You should see:**

```
configs/train.yaml:9:hf_token: hf_LABfakeTokenNotReal0000000000
```

That's the file, line 9, and a pasted Hugging Face token (`hf_...`).

✏️ **Mission 3 answer:** `configs/train.yaml`

Configs get shared, copied and committed to Git. A token in a config is a
token on the internet. Move it into `.env`, which `.gitignore` already keeps out of Git:

```bash
grep hf_token configs/train.yaml | sed 's/hf_token: /HF_TOKEN=/' > .env
sed -i '/^hf_token:/d' configs/train.yaml   # delete the line from the config
bash preflight.sh                           # one more FAIL: that's expected
```

| Piece | What it does |
|---|---|
| `grep hf_token configs/train.yaml` | finds the token line |
| `\| sed 's/hf_token: /HF_TOKEN=/'` | swaps `hf_token: ` for `HF_TOKEN=` |
| `> .env` | saves the result into a new file, `.env` |
| `sed -i '/^hf_token:/d'` | deletes that line from the config, in place |

**You should see:** `[FAIL] Secrets: .env is -rw-r--r--, so other users can read it`.
New files are readable by everyone. Lock it so only you can read it:

```bash
chmod 600 .env
ls -l .env                     # -rw-------
cat .gitignore                 # .env is listed, so Git ignores it
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

The second line is long: one command, three answers separated by spaces. **You should see:**

```
GO: all pre-flight checks passed. Safe to start the run.

Score: 3 / 3
Fix check: preflight.sh says GO. Run-08 is safe to start.
You just stopped a training run from dying at 97%.
```

`[MISS]`? Check the spelling of that path; the hint next to it names the command that finds it.
</details>

### Section 04 · Build it: read the pre-flight script

`preflight.sh` is about 70 lines of plain Bash, and every check uses a command
from this module: `df` and `du` for disk, `stat` for permissions, `grep` for
secrets. Read it, then make it yours:

```bash
less preflight.sh              # arrow keys scroll, q quits
```

Challenge: add a fourth check that fails if `scratch/` holds any `*.tmp` file
older than 7 days (`find scratch -name '*.tmp' -mtime +7`).

### Practice again

```bash
cd ~/linux-for-ai-ml/modules/module-2/scripts
python3 make_job.py --reset
```

Goal: from NO-GO to GO in under 5 minutes.

### Clean up

Done with the lab? Remove the practice job (about 40 MB), and clear any
token you exported:

```bash
cd ~/linux-for-ai-ml/modules/module-2/scripts
python3 make_job.py --clean
unset HF_TOKEN
```

**You should see:** `Removed /home/you/ai-job. Disk reclaimed.`
It only deletes a folder the lab built, and refuses anything else. Built it
somewhere else with `--dir`? Pass the same `--dir` to `--clean`.

### Stuck?

| You see | Do this |
|---|---|
| `make_job.py`: `already exists` | You built it before: `python3 make_job.py --reset` |
| `No configs/train.yaml here` | Wrong folder: `cd ~/ai-job`, then run it again |
| `cd ~/ai-job`: `No such file or directory` | Not built yet: do Step 2 |
| `cd ~/linux-for-ai-ml`: `No such file or directory` | Codespaces: `cd /workspaces/linux-for-ai-ml`. Otherwise do Module 1 Step 1 |
| `python3 train.py`: `can't open file` | This lab has no `train.py`. The check is `bash preflight.sh` |
| `check_answers.sh` shows `[MISS]` | A typo in a path. The hint next to it names the command that finds it |
| Stuck in a command? | Press **Ctrl + C** to cancel, then type the line again |

---

## Exercises (before Module 3)

1. **Free space**: `df -h ~` on your machine. How many GB are free?
2. **Read the bits**: `ls -l /etc/passwd /etc/shadow`. Why can you read one but not the other?
3. **Break & fix**: `touch x; chmod 000 x; cat x`, then fix it with `chmod 644 x`.
4. **Octal**: write `rwxr-x---` as a number. (Answer: 750.)
5. **Hunt secrets**: after your fix, `grep -rnE '(hf_|sk-)[A-Za-z0-9]{20,}' ~/ai-job/configs` finds nothing. Try it on your own projects too.
6. **Env vars**: `export DEMO=hi; echo $DEMO; unset DEMO; echo $DEMO`
7. **Break & fix**: `make_job.py --reset`, then reach GO again in 5 min.

**Self-check (from memory):** *A training run is about to start. What three things do you check first?*

<details><summary>Answer</summary>

Will it fit (`df -h`, `du -sh`)? Can it read its data (`ls -l`)? Are the secrets out of the configs (`grep`, `.env` with `chmod 600`)?
</details>

**Next:** Module 3 moves from *file at rest* to *process at work*.

---

📚 Part of **Linux for AI-ML Systems**, a T2S course. Subscribe at
**[transformed2succeed.com/membership](https://www.transformed2succeed.com/membership)** for access to all courses.
