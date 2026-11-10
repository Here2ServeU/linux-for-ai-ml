# Module 2 Workbook · Feed the Model

Use this workbook beside the [lab guide](README.md) and the slides.
Tick each box when you've done it, and write your answers in the blanks.
Print it, or copy it into your own notes. The steps match the slides and the README.

**Memory hook:** Will it fit? Can it read? Is it secret?

---

## Before you start

- [ ] I opened my Linux shell (Codespaces, WSL, Multipass or Linux).
- [ ] I know `#` starts a comment, so I don't type it.
- [ ] I type one line at a time and press **Enter**.

In your own words, what does `~` mean? ______________________________

---

## Step 1 · Get the lab

```bash
cd ~/linux-for-ai-ml
git pull
bash setup/doctor.sh
```

- [ ] Every doctor line says `OK`.

---

## Step 2 · Build the training job

```bash
cd ~/linux-for-ai-ml/modules/module-2/scripts
python3 make_job.py
cd ~/ai-job
cat README-FIRST.txt
ls
```

- [ ] I saw `Built your training job at ...`
- [ ] I read the briefing in `README-FIRST.txt`.

My job folder's full path is: ______________________________

How big is the scratch quota? ________ MB. How much does run-08 need? ________ MB.

```bash
bash preflight.sh
```

- [ ] I saw three `[FAIL]` lines and `NO-GO`.

How many checks failed? ________

---

## Step 3 · Mission 1: Will it fit?

```bash
grep -rn ERROR logs
df -h .
du -sh scratch/* | sort -h
```

| Question | Your answer |
|---|---|
| What error killed run-07? | |
| Is the disk itself full? (yes / no) | |
| Biggest folder in `scratch/`, and its size | |

✏️ **Mission 1 answer (a folder):** ______________________________

```bash
grep -rn run-03 configs
rm -r scratch/run-03-tmp
bash preflight.sh
```

- [ ] `grep` printed nothing, so no config uses the folder.
- [ ] The Disk line now says `[OK]`. MB left in scratch: ________

Why do we check *before* `rm -r`? ______________________________

---

## Step 4 · Mission 2: Can it read?

```bash
ls -l datasets
```

Write the ten permission characters for each file:

| File | Permissions | Can the owner read it? |
|---|---|---|
| `eval.jsonl` | | |
| `train.jsonl` | | |

✏️ **Mission 2 answer (a file):** ______________________________

Fill in the numbers: r = ____  w = ____  x = ____  →  `rw-r--r--` = ________

```bash
chmod 644 datasets/train.jsonl
ls -l datasets/train.jsonl
bash preflight.sh
```

- [ ] `train.jsonl` now shows `-rw-r--r--`.
- [ ] Both Permissions lines say `[OK]`.

Why never `chmod 777`? ______________________________

---

## Step 5 · Mission 3: Is it secret?

```bash
grep -rn token configs
```

✏️ **Mission 3 answer (a file):** ______________________________

On which line was the token? ________

```bash
grep hf_token configs/train.yaml | sed 's/hf_token: /HF_TOKEN=/' > .env
sed -i '/^hf_token:/d' configs/train.yaml
bash preflight.sh
```

- [ ] I saw `[FAIL] Secrets: .env is -rw-r--r--` (expected).

```bash
chmod 600 .env
ls -l .env
cat .gitignore
```

- [ ] `.env` shows `-rw-------`.
- [ ] `.env` is listed in `.gitignore`.

What does `600` mean, in plain words? ______________________________

---

## Step 6 · GO, then score

```bash
bash preflight.sh
bash check_answers.sh scratch/run-03-tmp datasets/train.jsonl configs/train.yaml
```

- [ ] `GO: all pre-flight checks passed.`
- [ ] `Score: 3 / 3`

My score: ____ / 3  ·  Time from NO-GO to GO: ________ minutes

---

## Section 04 · Read the pre-flight script

```bash
less preflight.sh
```

Which command does each check use?

| Check | Command(s) |
|---|---|
| Disk | |
| Permissions | |
| Secrets | |

- [ ] Challenge (optional): I added a fourth check with `find scratch -name '*.tmp' -mtime +7`.

---

## Practice and clean up

- [ ] `python3 make_job.py --reset`, then NO-GO to GO again in under 5 minutes. My time: ________
- [ ] Done: `python3 make_job.py --clean` and `unset HF_TOKEN`.

---

## Exercises (before Module 3)

| # | Exercise | Your answer |
|:-:|---|---|
| 1 | `df -h ~` How many GB are free? | |
| 2 | `ls -l /etc/passwd /etc/shadow` Why can you read only one? | |
| 3 | `touch x; chmod 000 x; cat x`, then `chmod 644 x` What error did you get first? | |
| 4 | `rwxr-x---` as a number | |
| 5 | `grep -rnE '(hf_\|sk-)[A-Za-z0-9]{20,}' ~/ai-job/configs` after your fix: anything found? | |
| 6 | `export DEMO=hi; echo $DEMO; unset DEMO; echo $DEMO` What printed? | |
| 7 | `make_job.py --reset`, then GO again. Time? | |

---

## Self-check (from memory)

A training run is about to start. What three things do you check first?

1. ______________________________
2. ______________________________
3. ______________________________

Bonus: which `chmod` number for a `.env` file, and why? ______________________________

Answers are at the end of the [lab guide](README.md#exercises-before-module-3).
